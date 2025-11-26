import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def fit_transform(self, X, y, test_size=0.2, random_state=42):
        """Basic preprocessing - handle -1s and scale"""
        # Replace -1 with NaN, then fill with median
        X_processed = X.replace(-1, np.nan)
        X_processed = X_processed.fillna(X_processed.median())

        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_processed, y, test_size=test_size, random_state=random_state, stratify=y
        )  # stratify prevents overfitting for imbalanced classes, splits positives proportionally

        return X_train, X_val, y_train, y_val

    def transform(self, X):
        """Transform test data"""
        X_processed = X.replace(-1, np.nan)
        X_processed = X_processed.fillna(X_processed.median())
        return X_processed
