import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine('postgresql://postgres:postgres123@localhost:5432/loandb')

# Load CSV
print("Loading CSV...")
df = pd.read_csv(r"C:\Users\Puchu\Desktop\loan-default-mlops\data\application_train.csv", usecols=[
    'TARGET', 'AMT_CREDIT', 'AMT_INCOME_TOTAL',
    'AMT_ANNUITY', 'DAYS_BIRTH', 'DAYS_EMPLOYED'
]).dropna()

# Save to PostgreSQL
print("Saving to PostgreSQL...")
df.to_sql('loan_applications', engine, if_exists='replace', index=False)
print(f"Done! {len(df)} rows saved to loandb.loan_applications")