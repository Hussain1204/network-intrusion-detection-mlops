from setuptools import find_packages, setup

setup(
    name="network-intrusion-detection-mlops",
    version="0.1.0",
    description="ML-based network intrusion detection system built using Python and MLOps principles.",
    packages=find_packages(exclude=("tests", "tests.*")),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.110,<1.0",
        "uvicorn[standard]>=0.27,<1.0",
        "python-multipart>=0.0.9",
        "jinja2>=3.1,<4.0",
        "pandas>=2.0,<3.0",
        "numpy>=1.24,<3.0",
        "scikit-learn>=1.3,<2.0",
        "joblib>=1.3,<2.0",
    ],
)
