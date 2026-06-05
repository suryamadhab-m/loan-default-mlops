import mlflow.xgboost
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from xgboost import XGBClassifier

app = FastAPI()

# Load model directly from file
model = XGBClassifier()
model.load_model("models/model.xgb")

class LoanData(BaseModel):
    AMT_CREDIT: float
    AMT_INCOME_TOTAL: float
    AMT_ANNUITY: float
    DAYS_BIRTH: int
    DAYS_EMPLOYED: int

@app.get("/")
def root():
    return {"message": "Loan Default Prediction API"}

@app.post("/predict")
def predict(data: LoanData):
    df = pd.DataFrame([data.dict()])
    prob = model.predict_proba(df)[:, 1][0]
    prediction = "DEFAULT" if prob > 0.5 else "NO DEFAULT"
    return {
        "probability": round(float(prob), 4),
        "prediction": prediction
    }