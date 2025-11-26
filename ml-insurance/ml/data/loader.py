import pandas as pd
from pathlib import Path


def load_data(data_path: str = "data/raw/porto-seguro-safe-driver-prediction"):
    """Load train and test datasets"""
    train = pd.read_csv(Path(data_path) / "train.csv")
    test = pd.read_csv(Path(data_path) / "test.csv")

    # Separate features and target
    X_train = train.drop(["id", "target"], axis=1)
    y_train = train["target"]
    X_test = test.drop(["id"], axis=1)

    return X_train, y_train, X_test, train["id"], test["id"]
