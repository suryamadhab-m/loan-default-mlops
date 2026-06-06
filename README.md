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
CSV Data (Kaggle)
      ↓
load_data.py → PostgreSQL Database (307,499 rows)
      ↓
train.py → Data Validation → XGBoost Training → MLflow Experiment Tracking
      ↓
MLflow Model Registry
      ↓
FastAPI REST API → Docker Container
      ↓
Evidently AI Drift Monitoring
      ↓
Auto Retraining (triggered on drift)
      ↓
GitHub Actions CI/CD (runs on every commit)
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Database | PostgreSQL 18 |
| Model | XGBoost |
| Experiment Tracking | MLflow |
| API Serving | FastAPI |
| Containerisation | Docker |
| Drift Monitoring | Evidently AI 0.4.30 |
| CI/CD | GitHub Actions |
| DB ORM | SQLAlchemy + psycopg2 |
| Language | Python 3.12 |

---

## Project Structure

```
loan-default-mlops/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD pipeline
├── data/                   # Dataset folder (not tracked in git)
├── models/
│   └── model.xgb           # Saved XGBoost model file
├── notebooks/              # EDA notebooks
├── src/
│   ├── load_data.py        # Load CSV into PostgreSQL database
│   ├── train.py            # Model training + MLflow tracking
│   ├── app.py              # FastAPI prediction service
│   └── monitor.py          # Evidently AI drift report
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.12
- PostgreSQL 18 (running locally on port 5432)
- Docker Desktop
- Kaggle account (for dataset download)

### 1. Clone the repository
```bash
git clone https://github.com/suryamadhab-m/loan-default-mlops.git
cd loan-default-mlops
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add PostgreSQL to PATH (Windows)
```bash
$env:PATH += ";C:\Program Files\PostgreSQL\18\bin"
```

### 4. Create the database
```bash
psql -U postgres -c "CREATE DATABASE loandb;"
```

### 5. Download dataset
Download `application_train.csv` from the [Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk/data) competition on Kaggle and place it in the `data/` folder.

### 6. Load data into PostgreSQL (first time only)
```bash
python src/load_data.py
```
This loads 307,499 rows into the `loandb.loan_applications` table.

### 7. Train the model
```bash
python src/train.py
```

### 8. View experiments in MLflow
```bash
python -m mlflow ui
```
Open `http://127.0.0.1:5000`

### 9. Start the prediction API
```bash
python -m uvicorn src.app:app --reload
```
Open `http://127.0.0.1:8000/docs`

### 10. Generate drift report
```bash
python src/monitor.py
start drift_report.html
```

### 11. Run with Docker
```bash
docker build -t loan-default-api .
docker run -p 8000:8000 loan-default-api
```

---

## API Usage

### Check API is running

**Endpoint:** `GET /`

**Response:**
```json
{"message": "Loan Default Prediction API"}
```

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
| Algorithm | XGBoost (n_estimators=100) |
| Features used | 5 of 122 available |
| Training rows | 307,499 |
| Test split | 80/20 |
| Database | PostgreSQL 18 (loandb) |

---

## CI/CD Pipeline

Every push to `main` automatically:
1. Sets up Python 3.12 environment
2. Starts a PostgreSQL 15 service container
3. Installs all dependencies including psycopg2-binary
4. Downloads the dataset from Kaggle using API secrets
5. Loads data into the CI PostgreSQL database
6. Runs the training script end-to-end
7. Reports success or failure

**Required GitHub Secrets:**
- `KAGGLE_USERNAME` — your Kaggle username
- `KAGGLE_KEY` — your Kaggle API key

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| DB_URL | postgresql://postgres:postgres123@localhost:5432/loandb | PostgreSQL connection string |

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

**Suryamadhab Moharana**
B.Tech Computer Science, ITER — SOA University (2027 batch)
TCS Xcelerate Capstone — MLOps Domain
GitHub: suryamadhab-m