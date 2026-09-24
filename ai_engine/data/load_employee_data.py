import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from sqlalchemy import text
from database.connection import engine

connection = engine.connect()

employee_id = "EMP001"

# Login count
login = connection.execute(
    text("""
    SELECT COUNT(*)
    FROM login_logs
    WHERE employee_id=:id
    """),
    {"id": employee_id}
).scalar()

# Files opened
files = connection.execute(
    text("""
    SELECT COUNT(*)
    FROM file_activity
    WHERE employee_id=:id
    """),
    {"id": employee_id}
).scalar()

# USB usage
usb = connection.execute(
    text("""
    SELECT COUNT(*)
    FROM usb_activity
    WHERE employee_id=:id
    """),
    {"id": employee_id}
).scalar()

connection.close()

employee = {

    "login_hour": login,

    "files_opened": files,

    "usb_used": usb,

    "failed_logins": 0

}

print(employee)