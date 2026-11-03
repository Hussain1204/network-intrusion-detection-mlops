# Network Security MLOps

A small, runnable network-traffic classification project with a local training pipeline and a FastAPI prediction service. The included CSV dataset makes the core workflow work without MongoDB, AWS, or external credentials.

## Project layout

```text
.
├── app.py                       # FastAPI health, training, and prediction endpoints
├── main.py                      # CLI training entry point
├── networksecurity/
│   ├── data.py                  # CSV loading and input validation
│   └── pipeline.py              # Training, metrics, persistence, and inference
├── data/
│   ├── data_schema/schema.yaml  # Dataset feature schema
│   └── phisingData.csv          # Included labeled dataset
├── tests/                       # Automated tests
├── testing/test.csv             # Example prediction input
├── requirements.txt
├── setup.py
└── Dockerfile
```

## Requirements and local setup

Python 3.10 or newer is supported. From the repository root:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

No `.env` file or MongoDB account is required for the local workflow.

## Train a model

```bash
python main.py
```

Training reads `data/phisingData.csv`, expects a numeric `Result` target column, evaluates a held-out split, and writes `artifacts/network_model.joblib`. You can supply a different labeled CSV or output path:

```bash
python main.py --data path/to/labeled.csv --model artifacts/custom-model.joblib
```

## Start the API

Train first, then run:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

- Interactive API docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>
- `POST /train` trains from the included dataset and saves the artifact.
- `POST /predict` accepts a CSV upload with the same feature columns as the training data. The target column may be omitted or included; if included it is ignored. The response is JSON containing the predicted labels.

Example prediction with the included feature-only sample:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F 'file=@testing/test.csv'
```

Prediction returns HTTP 503 until a model has been trained. Invalid CSVs and mismatched feature columns return HTTP 400.

## Tests

```bash
pytest
```

## Docker

Build and start the API (the image includes the dataset, so `/train` is available):

```bash
docker build -t network-security-mlops .
docker run --rm -p 8000:8000 network-security-mlops
```

Then train via `POST /train`, or train locally and mount the generated `artifacts` directory into the container if you want to serve a pre-trained model.

## Optional MongoDB integration

The default workflow intentionally uses the checked-in CSV to avoid requiring hosted services. MongoDB credentials should be supplied through environment variables if a future ingestion integration is enabled; never commit secrets. Use `.env.example` as a safe placeholder only.
