from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from pathlib import Path
from starlette.middleware.cors import CORSMiddleware

# Global variables for model and preprocessor
model = None
preprocessor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model and preprocessor
    global model, preprocessor
    model_path = Path("data/models/xgboost_model.pkl")
    preprocessor_path = Path("data/models/preprocessor.pkl")

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    if not preprocessor_path.exists():
        raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}")

    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    print("✓ Model and preprocessor loaded successfully")

    yield

    # Shutdown: Clean up resources
    print("Shutting down and cleaning up resources...")


app = FastAPI(title="Insurance Risk Prediction API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    features: dict  # Feature names and values


class PredictionResponse(BaseModel):
    claim_probability: float
    risk_level: str


@app.get("/")
def root():
    return {"message": "Insurance ML API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        # Convert to DataFrame
        df = pd.DataFrame([request.features])

        # Preprocess
        df_processed = preprocessor.transform(df)

        # Predict
        probability = float(model.predict_proba(df_processed)[0, 1])

        # Determine risk level
        if probability < 0.1:
            risk = "low"
        elif probability < 0.3:
            risk = "medium"
        else:
            risk = "high"

        return PredictionResponse(
            claim_probability=round(probability, 4), risk_level=risk
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sample")
def get_sample():
    """Return a sample row for testing"""
    train = pd.read_csv("data/raw/porto-seguro-safe-driver-prediction/train.csv")
    # get a random int between 0 and len(train)-1
    random_int = np.random.randint(0, len(train) - 1)
    sample = train.drop(["id", "target"], axis=1).iloc[random_int].to_dict()

    return {"features": sample}


@app.get("/features")
def get_feature_names():
    """Return list of feature names"""
    train = pd.read_csv("data/raw/porto-seguro-safe-driver-prediction/train.csv")
    features = train.drop(["id", "target"], axis=1).columns.tolist()

    return {"features": features}


# Just for local testing
@app.get("/predict/sample")
def predict_sample():
    """Test endpoint with a hardcoded sample"""
    sample = (
        pd.read_csv("data/raw/porto-seguro-safe-driver-prediction/train.csv")
        .drop(["id", "target"], axis=1)
        .iloc[0]
        .to_dict()
    )
    df_processed = preprocessor.transform(pd.DataFrame([sample]))
    probability = float(model.predict_proba(df_processed)[0, 1])

    return {"claim_probability": probability, "sample_used": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
