"""Optional MongoDB connectivity check.

Set MONGODB_URL_KEY in the environment to enable this check. No credentials
or network connection are required for normal development or tests.
"""

import os


def main() -> int:
    uri = os.getenv("MONGODB_URL_KEY")
    if not uri:
        print("Skipped: set MONGODB_URL_KEY to test a MongoDB connection.")
        return 0

    from pymongo import MongoClient

    try:
        with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
            client.admin.command("ping")
        print("MongoDB connection succeeded.")
        return 0
    except Exception as exc:
        print(f"MongoDB connection failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
