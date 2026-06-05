import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load reference data (original training data sample)
reference = pd.read_csv("data/application_train.csv", usecols=[
    'AMT_CREDIT', 'AMT_INCOME_TOTAL', 'AMT_ANNUITY', 
    'DAYS_BIRTH', 'DAYS_EMPLOYED'
]).dropna().sample(1000, random_state=42)

# Simulate current data with slight drift
current = reference.copy()
current['AMT_CREDIT'] = current['AMT_CREDIT'] * 1.3
current['AMT_INCOME_TOTAL'] = current['AMT_INCOME_TOTAL'] * 0.8

# Generate drift report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)
report.save_html("drift_report.html")

print("Drift report saved to drift_report.html")