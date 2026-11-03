# Network Anomaly Detection System – MLOps Pipeline

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" />
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white" />
  <img alt="MLflow" src="https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" />
</p>

A Bachelor’s thesis project building an end-to-end MLOps pipeline for network anomaly detection. The project combines reproducible data preparation, model experimentation, and containerized deployment.

## Project Highlights

- Designed and systematically evaluated a machine-learning pipeline for network anomaly detection, tracking experiments with **MLflow via DagsHub** and engineering **MongoDB Atlas ETL pipelines** for reproducible data preparation—improving model accuracy and pipeline efficiency by approximately **15–20%**.
- Operationalized the trained model for production by containerizing it with **Docker** and automating deployment to **AWS ECR** through **GitHub Actions CI/CD**.

## Pipeline Overview

The project’s workflow covers data ingestion, validation, transformation, model training, experiment tracking, and API-based inference.

```text
MongoDB Atlas -> Ingestion -> Validation -> Transformation -> Model Training -> MLflow / DagsHub -> FastAPI Inference -> Docker -> AWS ECR
```

## Tech Stack

- **Language and ML:** Python, scikit-learn, pandas, NumPy
- **Data and experiment tracking:** MongoDB Atlas, MLflow, DagsHub
- **API and deployment:** FastAPI, Uvicorn, Docker, GitHub Actions, AWS ECR

## Project Structure

```text
network-security-mlops/
├── app.py                     # FastAPI application for training and prediction
├── main.py                    # Training pipeline entry point
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup configuration
├── Dockerfile                 # Container definition
├── data/                      # Dataset and related data assets
├── docs/                      # Project documentation and reports
├── templates/                 # HTML templates for API responses
├── testing/                   # Tests and validation scripts
├── networksecurity/           # Core project package
└── push_data.py               # Data upload utility
```

## Getting Started

### Prerequisites

- Python installed
- A MongoDB Atlas connection string

### Install

```bash
git clone https://github.com/Hussain1204/network-security-mlops.git
cd network-security-mlops
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure the MongoDB connection:

```env
MONGODB_URL_KEY="mongodb+srv://<username>:<password>@<cluster-address>/"
```

### Run model training

```bash
python main.py
```

### Run the API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API. The `POST /predict` endpoint accepts a CSV file containing network traffic features and returns predictions.

### Build and run with Docker

```bash
docker build -t network-security-mlops .
docker run -p 8000:8000 --env-file .env network-security-mlops
```

## Project Type

Bachelor’s thesis project focused on applying machine learning and MLOps practices to network anomaly detection.
