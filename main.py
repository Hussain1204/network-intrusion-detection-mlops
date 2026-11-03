"""Command-line entry point for training the intrusion detection model."""

import argparse
import json

from networksecurity.pipeline import DEFAULT_DATASET, DEFAULT_MODEL_PATH, train_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the network intrusion classifier.")
    parser.add_argument("--data", default=str(DEFAULT_DATASET), help="Path to a labeled CSV dataset.")
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH), help="Output path for the model artifact.")
    args = parser.parse_args()
    print(json.dumps(train_model(args.data, args.model), indent=2))


if __name__ == "__main__":
    main()
