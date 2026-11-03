"""Data loading and validation for the local network-security workflow."""

from pathlib import Path

import pandas as pd

TARGET_COLUMN = "Result"


def load_dataset(path: str | Path, target_column: str = TARGET_COLUMN) -> tuple[pd.DataFrame, pd.Series]:
    """Load a labeled CSV and return numeric features and labels.

    An optional saved dataframe index (for example ``Unnamed: 0``) is removed.
    """
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    frame = pd.read_csv(csv_path)
    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed(:|$)")]
    if target_column not in frame.columns:
        raise ValueError(
            f"Missing target column {target_column!r}. Available columns: {list(frame.columns)}"
        )
    if len(frame) < 2:
        raise ValueError("The dataset must contain at least two rows.")

    labels = frame.pop(target_column)
    if labels.isna().any():
        raise ValueError(f"Target column {target_column!r} contains missing values.")
    if frame.empty:
        raise ValueError("The dataset must contain at least one feature column.")

    non_numeric = frame.select_dtypes(exclude=["number", "bool"]).columns.tolist()
    if non_numeric:
        raise ValueError(f"Features must be numeric. Unsupported columns: {non_numeric}")
    return frame, labels
