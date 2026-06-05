import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
import mlflow
import mlflow.xgboost

# Load data
df = pd.read_csv(r"C:\Users\Puchu\Desktop\loan-default-mlops\data\application_train.csv")

# Basic preprocessing
df = df[['TARGET', 'AMT_CREDIT', 'AMT_INCOME_TOTAL', 
         'AMT_ANNUITY', 'DAYS_BIRTH', 'DAYS_EMPLOYED']]
df = df.dropna()

# Split features and target
X = df.drop('TARGET', axis=1)
y = df['TARGET']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# MLflow tracking
mlflow.set_experiment("loan-default")

with mlflow.start_run():
    model = XGBClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    
    mlflow.log_metric("auc", auc)
    mlflow.xgboost.log_model(model, "model")
    
    print(f"AUC Score: {auc:.4f}")