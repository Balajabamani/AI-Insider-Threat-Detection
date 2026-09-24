import os
import sys
from datetime import datetime

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from sqlalchemy import text
from database.connection import engine

# Simulated Employee Login
employee = {
    "employee_id": "EMP001",
    "device_name": "HR-Laptop",
    "ip_address": "192.168.1.100",
    "login_status": "Success"
}

try:

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO login_logs
                (employee_id, ip_address, device_name, login_status)

                VALUES
                (:employee_id,
                 :ip_address,
                 :device_name,
                 :login_status)
            """),
            employee
        )

        connection.commit()

    print("=" * 50)
    print("Login Saved Successfully!")
    print("=" * 50)

    print(employee)

except Exception as e:

    print("Database Error")
    print(e)