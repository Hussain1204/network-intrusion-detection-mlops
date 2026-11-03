# Network Security Enhancement with MLOps

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white" />
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.2%2B-F7931E?logo=scikit-learn&logoColor=white" />
  <img alt="MLflow" src="https://img.shields.io/badge/MLflow-Tracking-0194E2?logo=mlflow&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" />
</p>

An end-to-end machine learning solution for network intrusion detection built with MLOps principles. This project focuses on detecting malicious or suspicious network traffic by combining robust data preprocessing, model training, experiment tracking, and a lightweight inference API for real-time predictions.

## Why this project?

Traditional rule-based intrusion detection systems often struggle to detect new and evolving cyber threats. This project applies machine learning and MLOps practices to create a scalable, reproducible, and maintainable intrusion detection pipeline.

## Key Features

- Data ingestion and validation for network traffic datasets
- Feature engineering and preprocessing pipeline
- Model training and evaluation using scikit-learn
- Experiment tracking with MLflow
- REST API for inference using FastAPI
- MongoDB-backed data workflow
- Containerized deployment with Docker
- Reproducible ML pipeline for experimentation and iteration

## Architecture Overview

The system follows an MLOps-driven workflow:

1. Collect and ingest network data
2. Validate incoming data quality
3. Transform and preprocess features
4. Train and evaluate ML models
5. Save and version model artifacts
6. Serve predictions through an API
7. Deploy the application in a reproducible environment

```text
Data Sources -> Ingestion -> Validation -> Transformation -> Model Training -> MLflow Tracking -> FastAPI Inference -> Deployment
```

## Tech Stack

- Python
- scikit-learn
- pandas / numpy
- MongoDB
- MLflow
- FastAPI
- Uvicorn
- Docker
- Python-dotenv

## Project Structure

```text
network-security-mlops/
├── app.py                     # FastAPI application for training and prediction
├── main.py                    # Training pipeline entry point
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup config
├── Dockerfile                 # Container definition
├── data/                     # Dataset and related data assets
├── docs/                     # Project documentation and reports
├── templates/                # HTML templates for API responses
├── testing/                  # Test files and validation scripts
├── networksecurity/          # Core project package
├── prediction_output/        # Inference output CSVs
├── final_model/              # Trained model artifacts
├── README.md                 # Project documentation
└── push_data.py              # Data upload utility
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

Create a `.env` file in the project root and add your MongoDB connection:

```bash
MONGODB_URL_KEY="mongodb+srv://<username>:<password>@<cluster-address>/"
```

## Run the Training Pipeline

```bash
python main.py
```

This triggers the project’s training workflow, including ingestion, validation, transformation, and model training.

## Run the Inference API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open the Swagger docs here:

- http://localhost:8000/docs

### Prediction endpoint

- `POST /predict`
- Upload a CSV file containing network traffic feature data
- The system processes the input and returns a table with predictions

## MLOps Workflow

This project incorporates core MLOps practices such as:

- Data pipeline automation
- Reproducible model training
- Artifact tracking with MLflow
- Standardized deployment through Docker
- API-based serving for predictions
- Separation of training and inference logic

## Docker

Build the container:

```bash
docker build -t network-security-mlops .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env network-security-mlops
```

## Project Impact

This project demonstrates how machine learning can be used for network security applications by improving anomaly detection capabilities while keeping the workflow structured, scalable, and operationally friendly.

## Notes

This repository is designed as a practical academic and research-oriented MLOps project for network intrusion detection. It is suitable for learning, experimentation, and extension into larger production-grade security systems.

---

If you want, I can also turn this into a more premium GitHub-style README with badges, a hero section, architecture diagram markup, and a clean project showcase layout.
