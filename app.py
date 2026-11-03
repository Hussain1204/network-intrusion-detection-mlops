"""FastAPI service for training and CSV-based intrusion detection."""

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse

from networksecurity.data import TARGET_COLUMN
from networksecurity.pipeline import DEFAULT_DATASET, DEFAULT_MODEL_PATH, predict, train_model

app = FastAPI(
    title="Network Security ML API",
    description="Train and run a network traffic anomaly classifier.",
    version="0.1.0",
)


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "model_trained": Path(DEFAULT_MODEL_PATH).is_file(),
    }


@app.post("/train", tags=["model"])
async def train() -> dict:
    """Train using the repository dataset and save the model locally."""
    try:
        return train_model(data_path=DEFAULT_DATASET, model_path=DEFAULT_MODEL_PATH)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc


@app.post("/predict", tags=["model"])
async def predict_csv(file: UploadFile = File(...)) -> dict:
    """Predict labels for a CSV upload and return rows plus predicted labels."""
    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(status_code=400, detail="Upload a .csv file.")
    try:
        frame = pd.read_csv(file.file)
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}") from exc
    finally:
        await file.close()

    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed(:|$)")]
    if TARGET_COLUMN in frame.columns:
        frame = frame.drop(columns=[TARGET_COLUMN])
    try:
        predictions = predict(frame, model_path=DEFAULT_MODEL_PATH)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {"count": len(predictions), "predictions": predictions}
