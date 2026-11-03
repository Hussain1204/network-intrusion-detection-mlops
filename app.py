"""FastAPI service for training and CSV-based intrusion detection."""

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.data import TARGET_COLUMN
from networksecurity.logger import logger
from networksecurity.pipeline import DEFAULT_DATASET, DEFAULT_MODEL_PATH, predict, train_model

app = FastAPI(
    title="Network Security ML API",
    description="Train and run a network traffic anomaly classifier.",
    version="0.1.0",
)

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    logger.info("Redirecting root request to dashboard")
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", tags=["ui"])
async def dashboard(request: Request):
    logger.info("Serving dashboard UI")
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "Network Security Dashboard"},
    )


@app.get("/health", tags=["health"])
async def health() -> dict[str, str | bool]:
    logger.info("Health check requested")
    return {
        "status": "ok",
        "model_trained": Path(DEFAULT_MODEL_PATH).is_file(),
    }


@app.post("/train", tags=["model"])
async def train_api() -> dict:
    logger.info("Training request received")
    try:
        result = train_model(data_path=DEFAULT_DATASET, model_path=DEFAULT_MODEL_PATH)
        logger.info("Training completed with metrics: %s", result)
        return result
    except (FileNotFoundError, ValueError) as exc:
        logger.warning("Training validation failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Training failed")
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc


@app.post("/predict", tags=["model"])
async def predict_csv(file: UploadFile = File(...)) -> dict:
    logger.info("Prediction request received for file: %s", file.filename)

    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        logger.warning("Upload rejected: %s", file.filename)
        raise HTTPException(status_code=400, detail="Upload a .csv file.")

    try:
        frame = pd.read_csv(file.file)
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        logger.warning("CSV parse failed: %s", exc)
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}") from exc
    finally:
        await file.close()

    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed(:|$)")]
    if TARGET_COLUMN in frame.columns:
        logger.info("Dropping target column before prediction")
        frame = frame.drop(columns=[TARGET_COLUMN])

    try:
        predictions = predict(frame, model_path=DEFAULT_MODEL_PATH)
        logger.info("Prediction completed for %s rows", len(predictions))
        return {"count": len(predictions), "predictions": predictions}
    except FileNotFoundError as exc:
        logger.error("Prediction requested before training: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        logger.warning("Prediction validation error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
