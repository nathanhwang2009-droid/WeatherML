"""Model training and inference utilities."""

import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def train_model(X: np.ndarray, y: np.ndarray, **kwargs) -> RandomForestRegressor:
    """Train a RandomForest regressor on the given data."""
    model = RandomForestRegressor(**kwargs)
    model.fit(X, y)
    return model


def save_model(model: RandomForestRegressor, path: Path | str) -> None:
    """Save a trained model to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(model, f)


def load_model(path: Path | str) -> RandomForestRegressor:
    """Load a trained model from disk."""
    with Path(path).open("rb") as f:
        return pickle.load(f)


def prepare_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42):
    """Split data into train and test sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
