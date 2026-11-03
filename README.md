# Network Anomaly Detection System – MLOps Pipeline

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" />
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white" />
  <img alt="MLflow" src="https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" />
</p>

A Bachelor’s thesis project focused on building an end-to-end MLOps pipeline for network anomaly detection. The project combines reproducible data preparation, model experimentation, API-based inference, and deployment automation to create a scalable and production-ready machine learning workflow.

## Project Highlights

- Designed and systematically evaluated a machine-learning pipeline for network anomaly detection, tracking experiments with **MLflow via DagsHub** and engineering **MongoDB Atlas ETL pipelines** for reproducible data preparation—improving model accuracy and pipeline efficiency by approximately **15–20%**.
- Operationalized the trained model for production by containerizing it with **Docker** and automating deployment to **AWS ECR** using **GitHub Actions CI/CD**.
- Built an end-to-end MLOps workflow for anomaly detection, integrating automated data preparation, model training, and experiment tracking to improve detection performance and reproducibility.
- Developed and evaluated the ML workflow using **Python, scikit-learn, and MLflow**, optimizing preprocessing and model training pipelines for better accuracy and efficiency.

## Project Overview

Traditional rule-based intrusion detection systems often struggle to detect evolving cyber threats. This project applies machine learning and MLOps practices to build a scalable, maintainable, and reproducible network security solution.

## Pipeline Architecture

```text
MongoDB Atlas -> Data Ingestion -> Validation -> Data Transformation -> Model Training -> MLflow / DagsHub -> FastAPI Inference -> Docker -> AWS ECR
```

## Tech Stack

- **Language and ML:** Python, scikit-learn, pandas, NumPy
- **Experiment tracking:** MLflow, DagsHub
- **Data workflow:** MongoDB Atlas
- **API and deployment:** FastAPI, Uvicorn, Docker, GitHub Actions, AWS ECR

## Key Features

- Network traffic data ingestion and validation
- Feature engineering and preprocessing pipeline
- Model training, evaluation, and artifact tracking
- Reproducible ETL workflow for data preparation
- FastAPI-based prediction service
- Containerized deployment and CI/CD automation

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
├── prediction_output/         # Inference output CSVs
├── final_model/               # Trained model artifacts
├── README.md                  # Project documentation
├── push_data.py               # Data upload utility
└── .env                       # Local environment variables
```

## Setup Instructions

### 1) Clone the repository

```bash
git clone https://github.com/Hussain1204/network-security-mlops.git
cd network-security-mlops
```

### 2) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the root directory:

```env
MONGODB_URL_KEY="mongodb+srv://<username>:<password>@<cluster-address>/"
```

## Run Model Training

```bash
python main.py
```

This triggers the training workflow, including ingestion, validation, transformation, and model training.

## Run the Inference API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open:

- http://localhost:8000/docs

The `POST /predict` endpoint accepts a CSV file with network feature data and returns predictions.

## Docker Deployment

```bash
docker build -t network-security-mlops .
docker run -p 8000:8000 --env-file .env network-security-mlops
```

## Project Type

Bachelor’s thesis project focused on applying machine learning and MLOps principles to network intrusion detection.

## Summary

This project demonstrates how machine learning can be used to improve network security by identifying anomalous behavior while maintaining a structured, scalable, and production-ready MLOps workflow.
