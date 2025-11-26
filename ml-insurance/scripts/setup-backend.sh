#!/bin/bash

# Change to parent directory
cd "$(dirname "$0")/.."
echo "Working directory: $(pwd)"

# Create new directories (only what's needed)
mkdir -p app/{api,models,services,core}
mkdir -p ml/{data,features,models,training,evaluation}
mkdir -p tests/{test_api,test_ml}
mkdir -p data/{raw,processed,models}
mkdir -p notebooks

# Create __init__.py files
touch app/__init__.py ml/__init__.py
touch app/api/__init__.py app/models/__init__.py app/services/__init__.py app/core/__init__.py
touch ml/data/__init__.py ml/features/__init__.py ml/models/__init__.py ml/training/__init__.py ml/evaluation/__init__.py
touch tests/__init__.py tests/test_api/__init__.py tests/test_ml/__init__.py

# Create core files
touch app/main.py app/core/config.py
touch ml/training/train.py ml/models/predictor.py ml/data/loader.py ml/features/preprocessor.py ml/evaluation/metrics.py
touch tests/test_api/test_endpoints.py tests/test_ml/test_model.py

# Create/activate venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Append to requirements.txt (or create if doesn't exist)
cat >> requirements.txt << EOF

# API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# ML Core
xgboost==2.0.3
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6
kaggle==1.5.16
EOF

pip install --upgrade pip
pip install -r requirements.txt

# Append to .gitignore if it exists, create if not
cat >> .gitignore << EOF

# ML Pipeline
data/raw/*
data/processed/*
data/models/*
notebooks/.ipynb_checkpoints/
kaggle.json
EOF

# Create .env if doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
APP_NAME=Insurance ML Pipeline
DEBUG=True
MODEL_PATH=data/models/xgboost_model.json
EOF
fi

echo "ML pipeline structure added!"
echo "To download dataset: kaggle competitions download -c porto-seguro-safe-driver-prediction -p data/raw"