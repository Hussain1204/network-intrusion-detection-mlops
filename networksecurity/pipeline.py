"""Train, persist, load, and use the intrusion-detection model."""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from networksecurity.data import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = PROJECT_ROOT / "data" / "phisingData.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "artifacts" / "network_model.joblib"


def train_model(
    data_path: str | Path = DEFAULT_DATASET,
    model_path: str | Path = DEFAULT_MODEL_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a reproducible classifier and persist model plus feature metadata."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be greater than 0 and less than 1.")

    features, labels = load_dataset(data_path)
    if labels.nunique() < 2:
        raise ValueError("Training requires at least two distinct target classes.")

    class_counts = labels.value_counts()
    stratify = labels if len(class_counts) > 1 and class_counts.min() >= 2 else None
    if stratify is not None and int(round(len(labels) * test_size)) < len(class_counts):
        stratify = None

    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=test_size, random_state=random_state, stratify=stratify
    )
    estimator = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("classifier", RandomForestClassifier(
                n_estimators=200,
                class_weight="balanced",
                random_state=random_state,
                n_jobs=-1,
            )),
        ]
    )
    estimator.fit(x_train, y_train)
    predictions = estimator.predict(x_test)

    destination = Path(model_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": estimator, "feature_names": features.columns.tolist(), "version": 1},
        destination,
    )

    return {
        "model_path": str(destination),
        "rows": int(len(features)),
        "features": int(features.shape[1]),
        "classes": [value.item() if hasattr(value, "item") else value for value in estimator.classes_],
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision_weighted": float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
    }


def load_model(model_path: str | Path = DEFAULT_MODEL_PATH) -> dict[str, Any]:
    """Load a previously trained model bundle."""
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(f"No trained model found at {path}. Run `python main.py` first.")
    bundle = joblib.load(path)
    if not isinstance(bundle, dict) or not {"model", "feature_names"}.issubset(bundle):
        raise ValueError(f"Invalid model artifact: {path}")
    return bundle


def predict(features: pd.DataFrame, model_path: str | Path = DEFAULT_MODEL_PATH) -> list[Any]:
    """Predict labels for records with the same named features used during training."""
    bundle = load_model(model_path)
    expected = bundle["feature_names"]
    missing = [name for name in expected if name not in features.columns]
    extra = [name for name in features.columns if name not in expected]
    if missing or extra:
        raise ValueError(f"Feature mismatch; missing={missing}, unexpected={extra}")
    values = features.loc[:, expected]
    non_numeric = values.select_dtypes(exclude=["number", "bool"]).columns.tolist()
    if non_numeric:
        raise ValueError(f"Features must be numeric. Unsupported columns: {non_numeric}")
    if values.empty:
        raise ValueError("At least one CSV row is required for prediction.")
    return bundle["model"].predict(values).tolist()
