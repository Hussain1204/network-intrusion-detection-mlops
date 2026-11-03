import io

import pandas as pd
from fastapi.testclient import TestClient

import app as api
from networksecurity.pipeline import train_model

client = TestClient(api.app)


def make_dataset(path):
    rows = []
    for label in (0, 1):
        for index in range(20):
            rows.append(
                {
                    "feature_a": label * 10 + index / 100,
                    "feature_b": label,
                    "Result": label,
                }
            )
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_dashboard_is_served():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Network Security Prediction Dashboard" in response.text


def test_root_redirects_to_dashboard():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/dashboard"


def test_training_persists_loadable_model(tmp_path):
    dataset = make_dataset(tmp_path / "train.csv")
    model_path = tmp_path / "model.joblib"
    metrics = train_model(dataset, model_path)

    assert model_path.is_file()
    assert metrics["rows"] == 40
    assert metrics["features"] == 2
    assert 0 <= metrics["accuracy"] <= 1


def test_predict_endpoint_returns_labels(tmp_path, monkeypatch):
    dataset = make_dataset(tmp_path / "train.csv")
    model_path = tmp_path / "model.joblib"
    train_model(dataset, model_path)
    monkeypatch.setattr(api, "DEFAULT_MODEL_PATH", model_path)
    csv = io.BytesIO(b"feature_a,feature_b\n0.01,0\n10.01,1\n")

    response = TestClient(api.app).post(
        "/predict", files={"file": ("traffic.csv", csv, "text/csv")}
    )

    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert len(response.json()["predictions"]) == 2


def test_predict_endpoint_requires_trained_model(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "DEFAULT_MODEL_PATH", tmp_path / "missing.joblib")
    csv = io.BytesIO(b"feature_a,feature_b\n0.01,0\n")

    response = TestClient(api.app).post(
        "/predict", files={"file": ("traffic.csv", csv, "text/csv")}
    )

    assert response.status_code == 503
