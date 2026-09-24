import os
import sys
import joblib
import pandas as pd

# Add project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

# Import employee data from database
from ai_engine.data.load_employee_data import employee

# Convert dictionary to DataFrame
employee = pd.DataFrame([employee])

# Load trained Isolation Forest model
model = joblib.load(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "models",
        "isolation_forest.pkl"
    )
)

# Predict
prediction = model.predict(employee)

print("=" * 60)
print("AI INSIDER THREAT DETECTION ENGINE")
print("=" * 60)

print("\nEmployee Data Received:\n")
print(employee)

print("\nPrediction Result:\n")

if prediction[0] == -1:
    print("⚠ Insider Threat Detected")
else:
    print("✅ Employee Behaviour Normal")

print("=" * 60)