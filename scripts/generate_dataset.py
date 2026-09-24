import random
import pandas as pd

employees = [
    "EMP001",
    "EMP002",
    "EMP003",
    "EMP004",
    "EMP005"
]

rows = []

for i in range(1000):

    login_hour = random.randint(8, 18)

    files_opened = random.randint(1, 20)

    usb_used = random.choice([0, 0, 0, 1])

    failed_logins = random.randint(0, 2)

    rows.append({

        "employee_id": random.choice(employees),

        "login_hour": login_hour,

        "files_opened": files_opened,

        "usb_used": usb_used,

        "failed_logins": failed_logins

    })

df = pd.DataFrame(rows)

df.to_csv(
    "../datasets/employee_activity.csv",
    index=False
)

print("="*50)
print("Dataset Generated Successfully")
print("="*50)

print(df.head())