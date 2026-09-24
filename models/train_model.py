import pandas as pd

from sklearn.ensemble import IsolationForest

import joblib

# Load dataset
df = pd.read_csv("../datasets/employee_activity.csv")

# Features used for training
X = df[
    [
        "login_hour",
        "files_opened",
        "usb_used",
        "failed_logins"
    ]
]

# Create Isolation Forest model
model = IsolationForest(

    n_estimators=100,

    contamination=0.05,

    random_state=42

)

# Train
model.fit(X)

# Save model
joblib.dump(model, "isolation_forest.pkl")

print("="*50)
print("Isolation Forest Model Trained Successfully")
print("="*50)