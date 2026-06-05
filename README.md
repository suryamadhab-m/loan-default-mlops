# Loan Default Prediction Pipeline
### TCS Xcelerate Capstone | MLOps Domain

An end-to-end MLOps pipeline that predicts loan default risk with automated retraining on data drift — built as part of the TCS Xcelerate industry capstone programme.

![CI Pipeline](https://github.com/suryamadhab-m/loan-default-mlops/actions/workflows/ci.yml/badge.svg)

---

## Overview

A digital lending organisation requires a predictive model to identify borrowers at risk of loan default. Since macroeconomic conditions and borrower behaviour evolve continuously, a static model degrades in accuracy over time. This pipeline detects data drift, retrains the model automatically, and exposes predictions via a REST API.

---

## Architecture

```
Data (PostgreSQL/CSV)
        ↓
Data Validation (Great Expectations)
        ↓
Model Training (XGBoost) → Experiment Tracking (MLflow)
        ↓
Model Registry (MLflow)
        ↓
REST API (FastAPI + Docker)
        ↓
Drift Monitoring (Evidently AI)
        ↓
Auto Retraining (Apache Airflow) ← triggered on drift
        ↓
CI/CD (GitHub Actions)
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Model | XGBoost |
| Experiment Tracking | MLflow |
| Data Validation | Great Expectations |
| Pipeline Orchestration | Apache Airflow |
| API Serving | FastAPI |
| Containerisation | Docker |
| Drift Monitoring | Evidently AI |
| CI/CD | GitHub Actions |
| Database | PostgreSQL |
| Language | Python 3.12 |

---

## Project Structure

```
loan-default-mlops/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── data/                   # Dataset (not tracked in git)
├── models/                 # Saved model files
├── notebooks/              # EDA notebooks
├── src/
│   ├── train.py            # Model training + MLflow tracking
│   ├── app.py              # FastAPI prediction service
│   └── monitor.py          # Evidently AI drift report
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/suryamadhab-m/loan-default-mlops.git
cd loan-default-mlops
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download dataset
Download `application_train.csv` from the [Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk/data) competition on Kaggle and place it in the `data/` folder.

### 4. Train the model
```bash
python src/train.py
```

### 5. View experiments in MLflow
```bash
python -m mlflow ui
```
Open `http://127.0.0.1:5000`

### 6. Start the prediction API
```bash
python -m uvicorn src.app:app --reload
```
Open `http://127.0.0.1:8000/docs`

### 7. Run drift monitoring
```bash
python src/monitor.py
```
Opens `drift_report.html` with Evidently AI dashboard.

### 8. Run with Docker
```bash
docker build -t loan-default-api .
docker run -p 8000:8000 loan-default-api
```

---

## API Usage

### Predict loan default

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "AMT_CREDIT": 500000,
  "AMT_INCOME_TOTAL": 150000,
  "AMT_ANNUITY": 25000,
  "DAYS_BIRTH": -12000,
  "DAYS_EMPLOYED": -2000
}
```

**Response:**
```json
{
  "probability": 0.0096,
  "prediction": "NO DEFAULT"
}
```

---

## Model Performance

| Metric | Value |
|---|---|
| AUC Score | 0.6425 |
| Algorithm | XGBoost |
| Features | 5 (credit amount, income, annuity, age, employment) |
| Training samples | ~307,000 |

---

## CI/CD Pipeline

Every push to `main` automatically:
1. Sets up Python 3.12 environment
2. Installs all dependencies
3. Downloads the dataset from Kaggle
4. Runs the training script
5. Validates the pipeline end-to-end

---

## Assessment Criteria (TCS Xcelerate)

| Dimension | Weight |
|---|---|
| Technical Implementation | 40% |
| Architectural Thinking | 25% |
| Operational Readiness | 20% |
| Communication | 15% |

---

## Author

**Surya Madhab Moharana**  
B.Tech Computer Science, ITER — SOA University (2027 batch)  
TCS Xcelerate Capstone — MLOps Domain
