install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

train:
	python main.py

run:
	uvicorn app:app --host 127.0.0.1 --port 8000 --reload

test:
	pytest -q

build:
	docker build -t network-intrusion-detection-mlops .

.PHONY: install train run test build
