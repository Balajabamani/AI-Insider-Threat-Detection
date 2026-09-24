import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)
from database.connection import engine
from sqlalchemy import text

# Simulated USB Event

usb = {
    "employee_id": "EMP001",
    "device_name": "SanDisk USB 64GB",
    "action": "CONNECTED"
}

try:

    connection = engine.connect()

    connection.execute(

        text("""

        INSERT INTO usb_activity
        (employee_id, device_name, action)

        VALUES
        (:employee_id,
         :device_name,
         :action)

        """),

        usb

    )

    connection.commit()

    print("=" * 50)
    print("USB Activity Saved Successfully!")
    print("=" * 50)
    print(usb)

except Exception as e:

    print("Database Error")
    print(e)