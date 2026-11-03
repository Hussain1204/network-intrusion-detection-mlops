"""Command-line entry point for model training."""

import argparse
import json

from networksecurity.pipeline import DEFAULT_DATASET, DEFAULT_MODEL_PATH, train_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the network intrusion classifier.")
    parser.add_argument("--data", default=str(DEFAULT_DATASET), help="Path to a labeled CSV dataset.")
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH), help="Where to save the model artifact.")
    args = parser.parse_args()
    metrics = train_model(data_path=args.data, model_path=args.model)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
