from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
requirements = [
    line.strip()
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]

setup(
    name="network-security-mlops",
    version="0.1.0",
    description="ML-based network intrusion detection system built using Python and MLOps principles.",
    packages=find_packages(exclude=("tests", "tests.*")),
    python_requires=">=3.10",
    install_requires=requirements,
)
