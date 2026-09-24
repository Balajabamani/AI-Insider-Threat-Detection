import joblib
import pandas as pd

# Load trained model
model = joblib.load("isolation_forest.pkl")

# Example employee activity
employee = pd.DataFrame([{

    "login_hour": 23,

    "files_opened": 48,

    "usb_used": 1,

    "failed_logins": 4

}])

prediction = model.predict(employee)

print("="*50)

if prediction[0] == -1:
    print("🚨 Suspicious Employee Activity Detected")
else:
    print("✅ Normal Employee Activity")

print("="*50)