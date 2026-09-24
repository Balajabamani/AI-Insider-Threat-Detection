import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from database.connection import engine
from sqlalchemy import text

employee = "EMP001"

connection = engine.connect()

# Count Login Events

login_count = connection.execute(

    text("""

    SELECT COUNT(*)

    FROM login_logs

    WHERE employee_id=:id

    """),

    {"id": employee}

).scalar()

# Count File Events

file_count = connection.execute(

    text("""

    SELECT COUNT(*)

    FROM file_activity

    WHERE employee_id=:id

    """),

    {"id": employee}

).scalar()

# Count USB Events

usb_count = connection.execute(

    text("""

    SELECT COUNT(*)

    FROM usb_activity

    WHERE employee_id=:id

    """),

    {"id": employee}

).scalar()

login_score = login_count * 5
file_score = file_count * 10
usb_score = usb_count * 20

total = login_score + file_score + usb_score

if total < 20:
    level = "LOW"

elif total < 50:
    level = "MEDIUM"

else:
    level = "HIGH"

connection.execute(

    text("""

    INSERT INTO risk_scores

    (employee_id,
     login_score,
     file_score,
     usb_score,
     total_score,
     risk_level)

    VALUES

    (:employee,
     :login,
     :file,
     :usb,
     :total,
     :level)

    """),

    {

        "employee": employee,
        "login": login_score,
        "file": file_score,
        "usb": usb_score,
        "total": total,
        "level": level

    }

)

connection.commit()

print("="*60)
print("RISK SCORE GENERATED")
print("="*60)

print("Employee :", employee)
print("Login Score :", login_score)
print("File Score :", file_score)
print("USB Score :", usb_score)
print("Total Score :", total)
print("Risk Level :", level)