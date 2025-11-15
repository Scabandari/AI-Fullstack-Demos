import xgboost as xgb
from sklearn.metrics import roc_auc_score
import joblib
from pathlib import Path
import sys

sys.path.append(".")

from ml.data.loader import load_data
from ml.features.preprocessor import Preprocessor


def train_model():
    # Load data
    print("Loading data...")
    X_train, y_train, X_test, train_ids, test_ids = load_data()

    # Preprocess
    print("Preprocessing...")
    preprocessor = Preprocessor()
    X_tr, X_val, y_tr, y_val = preprocessor.fit_transform(X_train, y_train)

    # Train XGBoost
    print("Training XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=100,  # diminishing returns if too high, start w/ 100
        max_depth=4,  # too deep --> overfitting (3-6 is a good range)
        learning_rate=0.1,  # each tree's contribution, lower = slower but more robust, typically 0.01-0.3
        objective="binary:logistic",  # loss functin tells EXGBoost this is a binary classification
        eval_metric="auc",  # What to print during training (doesn't affect optimization)
        random_state=42,  # key for reproducibility
        # so it doens't just predict 0 & be right 96% of the time
        scale_pos_weight=len(y_tr[y_tr == 0]) / len(y_tr[y_tr == 1]),
    )

    model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=True)

    # If validation AUC plateaus or declines, stop early or reduce n_estimators (it should continue to rise)

    # Evaluate
    val_preds = model.predict_proba(X_val)[:, 1]
    val_auc = roc_auc_score(y_val, val_preds)
    print(f"\nValidation AUC: {val_auc:.4f}")

    # Save model
    Path("data/models").mkdir(parents=True, exist_ok=True)
    joblib.dump(model, "data/models/xgboost_model.pkl")
    joblib.dump(preprocessor, "data/models/preprocessor.pkl")
    print("Model saved!")

    return model, val_auc


if __name__ == "__main__":
    train_model()
