"""FastAPI service for training and CSV-based intrusion detection."""

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.data import TARGET_COLUMN
from networksecurity.logger import logger
from networksecurity.pipeline import DEFAULT_DATASET, DEFAULT_MODEL_PATH, predict, train_model

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(
    title="Network Intrusion Detection API",
    description="Train and run a network traffic anomaly classifier.",
    version="0.1.0",
)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", tags=["ui"])
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"title": "Network Security Dashboard"},
    )


@app.get("/health", tags=["health"])
async def health() -> dict[str, str | bool]:
    return {"status": "ok", "model_trained": Path(DEFAULT_MODEL_PATH).is_file()}


@app.post("/train", tags=["model"])
async def train_api() -> dict:
    logger.info("Training requested")
    try:
        metrics = train_model(data_path=DEFAULT_DATASET, model_path=DEFAULT_MODEL_PATH)
        logger.info("Training completed: %s", metrics)
        return metrics
    except (FileNotFoundError, ValueError) as exc:
        logger.warning("Training input error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Training failed")
        raise HTTPException(status_code=500, detail="Training failed. Check server logs.") from exc


@app.post("/predict", tags=["model"])
async def predict_csv(file: UploadFile = File(...)) -> dict:
    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(status_code=400, detail="Upload a .csv file.")

    try:
        frame = pd.read_csv(file.file)
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}") from exc
    finally:
        await file.close()

    frame = frame.loc[:, ~frame.columns.astype(str).str.match(r"^Unnamed(:|$)")]
    frame = frame.drop(columns=[TARGET_COLUMN], errors="ignore")
    try:
        predictions = predict(frame, model_path=DEFAULT_MODEL_PATH)
        logger.info("Predicted labels for %d rows", len(predictions))
        return {"count": len(predictions), "predictions": predictions}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed. Check server logs.") from exc
