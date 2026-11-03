# Network Intrusion Detection MLOps

A runnable machine-learning project that trains a network-traffic classifier from the included labeled CSV and serves predictions through FastAPI and a small upload dashboard. The core workflow is local-first: MongoDB, AWS credentials, and hosted experiment trackers are not required.

## Project structure

```text
.
├── app.py                       # FastAPI API and dashboard routes
├── main.py                      # CLI training command
├── networksecurity/
│   ├── data.py                  # CSV loading and validation
│   ├── logger.py                # Shared application logger
│   └── pipeline.py              # Training, metrics, persistence, prediction
├── data/
│   ├── data_schema/schema.yaml
│   └── phisingData.csv          # Labeled training dataset
├── templates/dashboard.html
├── testing/test.csv             # Example feature-only prediction input
├── tests/test_application.py
├── requirements.txt
├── setup.py
└── Dockerfile
```

## Requirements and installation

Python 3.10 or newer is supported. From the repository root:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

No `.env` configuration is needed for local training or inference.

## Train a model

```bash
python main.py
```

The command reads `data/phisingData.csv`, expects a numeric `Result` label column, evaluates a held-out split, then writes `artifacts/network_model.joblib`.

Use a different labeled CSV or output path with:

```bash
python main.py --data path/to/labeled.csv --model artifacts/custom-model.joblib
```

## Run the API and dashboard

Train first, then start the server:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open <http://127.0.0.1:8000/dashboard>. API documentation is at <http://127.0.0.1:8000/docs>, and the health endpoint is <http://127.0.0.1:8000/health>.

Endpoints:

- `GET /health` reports service status and whether a model artifact exists.
- `POST /train` trains from the included dataset and saves the model.
- `POST /predict` accepts a CSV upload and returns predicted labels. Upload the same named feature columns used for training; the `Result` column may be included and will be ignored.

Example:

```bash
curl -X POST http://127.0.0.1:8000/predict \\
  -F 'file=@testing/test.csv'
```

Prediction returns HTTP 503 until a model has been trained. Invalid CSV and feature mismatches return HTTP 400.

## Tests

```bash
pytest -q
```

## Docker

The image includes application code and the training dataset. Start the API:

```bash
docker build -t network-intrusion-detection-mlops .
docker run --rm -p 8000:8000 network-intrusion-detection-mlops
```

Train through `POST /train` in the API docs or the dashboard does not trigger training automatically; run training in the container with:

```bash
docker run --rm network-intrusion-detection-mlops python main.py
```

To persist a trained artifact between container runs, mount a local directory at `/app/artifacts`:

```bash
mkdir -p artifacts
docker run --rm -p 8000:8000 -v "$(pwd)/artifacts:/app/artifacts" network-intrusion-detection-mlops
```

## Security and project scope

Do not commit passwords, tokens, private datasets, or `.env` files. The project makes no claim that its sample classifier replaces a properly evaluated and monitored production intrusion-detection system. Validate data quality, false-positive rates, model drift, and operational requirements before deployment.
