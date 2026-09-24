from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

import joblib
import pandas as pd
from datetime import datetime

from app.services.activity_monitor import get_monitor_snapshot


router = APIRouter()


# ============================================================
# AI MODEL
# ============================================================

MODEL_PATH = "models/isolation_forest.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("AI Isolation Forest model loaded successfully.")
except Exception as error:
    print("AI model could not be loaded:", error)
    model = None


# ============================================================
# EMPLOYEE INFORMATION
# ============================================================

EMPLOYEE_INFO = {

    "EMP001": {
        "name": "Alice",
        "department": "Finance",
        "role": "Accountant"
    },

    "EMP002": {
        "name": "Bob",
        "department": "HR",
        "role": "HR Executive"
    },

    "EMP003": {
        "name": "Charlie",
        "department": "IT",
        "role": "IT Administrator"
    },

    "EMP004": {
        "name": "David",
        "department": "Admin",
        "role": "Administrator"
    },

    "EMP005": {
        "name": "Emma",
        "department": "Sales",
        "role": "Sales Executive"
    }

}


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"


# ============================================================
# RISK FACTORS
# ============================================================

def build_risk_factors(
    login_events,
    file_events,
    usb_events,
    failed_logins,
    suspicious_deletions,
    suspicious_renames
):

    factors = []


    # --------------------------------------------------------
    # FAILED LOGIN
    # --------------------------------------------------------

    if failed_logins > 0:

        factors.append({

            "title":
                "Failed Login Activity",

            "description":
                f"{failed_logins} failed login "
                f"event(s) detected",

            "score":
                failed_logins * 15,

            "icon":
                "🔐"

        })


    # --------------------------------------------------------
    # USB
    # --------------------------------------------------------

    if usb_events > 0:

        factors.append({

            "title":
                "USB Device Activity",

            "description":
                f"{usb_events} external device "
                f"event(s) detected",

            "score":
                usb_events * 20,

            "icon":
                "🔌"

        })


    # --------------------------------------------------------
    # FILE DELETION
    # --------------------------------------------------------

    if suspicious_deletions > 0:

        factors.append({

            "title":
                "File Deletion",

            "description":
                f"{suspicious_deletions} suspicious "
                f"file deletion event(s) detected",

            "score":
                suspicious_deletions * 15,

            "icon":
                "🗑️"

        })


    # --------------------------------------------------------
    # FILE RENAME
    # --------------------------------------------------------

    if suspicious_renames > 0:

        factors.append({

            "title":
                "File Rename",

            "description":
                f"{suspicious_renames} suspicious "
                f"file rename event(s) detected",

            "score":
                suspicious_renames * 10,

            "icon":
                "📝"

        })


    # --------------------------------------------------------
    # GENERAL FILE ACTIVITY
    # --------------------------------------------------------

    if file_events > 0:

        factors.append({

            "title":
                "File Access Activity",

            "description":
                f"{file_events} file activity "
                f"event(s) monitored",

            "score":
                file_events * 5,

            "icon":
                "📁"

        })


    # --------------------------------------------------------
    # LOGIN ACTIVITY
    # --------------------------------------------------------

    if login_events > 0:

        factors.append({

            "title":
                "Login Activity",

            "description":
                f"{login_events} successful login "
                f"event(s) detected",

            "score":
                login_events * 5,

            "icon":
                "🔑"

        })


    return factors


# ============================================================
# DASHBOARD
# ============================================================

@router.get("/dashboard")
def dashboard():

    employee_id = "EMP001"

    employee_info = EMPLOYEE_INFO[employee_id]

    current_hour = datetime.now().hour


    # ========================================================
    # DATABASE COUNTS
    # ========================================================

    login_events = 0

    file_events = 0

    usb_events = 0

    failed_logins = 0


    db_activities = []


    try:

        with engine.connect() as connection:


            # ------------------------------------------------
            # LOGIN EVENTS
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT COUNT(*)
                        FROM login_logs
                        WHERE employee_id = :employee_id
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )

                login_events = (
                    result.scalar() or 0
                )

            except Exception as error:

                print(
                    "Login count error:",
                    error
                )


            # ------------------------------------------------
            # FAILED LOGINS
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT COUNT(*)
                        FROM login_logs
                        WHERE employee_id = :employee_id
                        AND LOWER(login_status) LIKE '%fail%'
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )

                failed_logins = (
                    result.scalar() or 0
                )

            except Exception as error:

                print(
                    "Failed login count error:",
                    error
                )


            # ------------------------------------------------
            # FILE EVENTS
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT COUNT(*)
                        FROM file_activity
                        WHERE employee_id = :employee_id
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )

                file_events = (
                    result.scalar() or 0
                )

            except Exception as error:

                print(
                    "File count error:",
                    error
                )


            # ------------------------------------------------
            # USB EVENTS
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT COUNT(*)
                        FROM usb_activity
                        WHERE employee_id = :employee_id
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )

                usb_events = (
                    result.scalar() or 0
                )

            except Exception as error:

                print(
                    "USB count error:",
                    error
                )


            # ------------------------------------------------
            # RECENT FILE ACTIVITY
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT
                            activity_time,
                            action,
                            file_name
                        FROM file_activity
                        WHERE employee_id = :employee_id
                        ORDER BY activity_time DESC
                        LIMIT 20
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )


                for row in result:

                    db_activities.append({

                        "time":
                            str(
                                row.activity_time
                            ),

                        "activity":
                            f"{row.action} - "
                            f"{row.file_name}"

                    })

            except Exception as error:

                print(
                    "File activity error:",
                    error
                )


            # ------------------------------------------------
            # RECENT USB ACTIVITY
            # ------------------------------------------------

            try:

                result = connection.execute(

                    text("""
                        SELECT
                            usb_time,
                            action,
                            device_name
                        FROM usb_activity
                        WHERE employee_id = :employee_id
                        ORDER BY usb_time DESC
                        LIMIT 20
                    """),

                    {
                        "employee_id":
                            employee_id
                    }

                )


                for row in result:

                    db_activities.append({

                        "time":
                            str(
                                row.usb_time
                            ),

                        "activity":
                            f"{row.action} - "
                            f"{row.device_name}"

                    })

            except Exception as error:

                print(
                    "USB activity error:",
                    error
                )


    except Exception as error:

        print(
            "Database connection error:",
            error
        )


    # ========================================================
    # REAL-TIME MONITOR
    # ========================================================

    monitor_data = get_monitor_snapshot()


    live_activities = monitor_data.get(
        "activities",
        []
    )


    live_counts = monitor_data.get(
        "counts",
        {}
    )


    # ========================================================
    # LIVE COUNTS
    # ========================================================

    live_login_events = int(
        live_counts.get(
            "login",
            0
        )
    )


    live_failed_logins = int(
        live_counts.get(
            "failed_login",
            0
        )
    )


    live_file_events = int(
        live_counts.get(
            "file",
            0
        )
    )


    live_usb_events = int(
        live_counts.get(
            "usb",
            0
        )
    )


    # ========================================================
    # COUNT LIVE SUSPICIOUS FILE EVENTS
    # ========================================================

    suspicious_deletions = 0

    suspicious_renames = 0


    for item in live_activities:

        activity_text = str(
            item.get(
                "activity",
                ""
            )
        ).upper()


        if activity_text.startswith(
            "DELETED -"
        ):

            suspicious_deletions += 1


        elif activity_text.startswith(
            "RENAMED -"
        ):

            suspicious_renames += 1


    # ========================================================
    # EFFECTIVE COUNTS
    # ========================================================

    effective_login_events = max(
        int(login_events),
        live_login_events
    )


    effective_failed_logins = max(
        int(failed_logins),
        live_failed_logins
    )


    effective_file_events = max(
        int(file_events),
        live_file_events
    )


    effective_usb_events = max(
        int(usb_events),
        live_usb_events
    )


    # ========================================================
    # RISK SCORE
    # ========================================================

    risk_score = (

        effective_login_events * 5

        +

        effective_file_events * 5

        +

        effective_usb_events * 20

        +

        effective_failed_logins * 15

        +

        suspicious_deletions * 15

        +

        suspicious_renames * 10

    )


    # Limit to 100

    risk_score = min(
        int(risk_score),
        100
    )


    # ========================================================
    # RISK LEVEL
    # ========================================================

    risk_level = get_risk_level(
        risk_score
    )


    # ========================================================
    # AI MODEL
    # ========================================================

    prediction = risk_level


    if model is not None:

        try:

            employee_df = pd.DataFrame({

                "login_hour":
                    [current_hour],

                "files_opened":
                    [effective_file_events],

                "usb_used":
                    [effective_usb_events],

                "failed_logins":
                    [effective_failed_logins]

            })


            model_prediction = model.predict(
                employee_df
            )[0]


            # Isolation Forest:
            #
            # -1 = anomaly
            #  1 = normal
            #
            # The final displayed prediction still
            # follows the calculated security risk.

            if model_prediction == -1:

                prediction = risk_level

            else:

                prediction = risk_level


        except Exception as error:

            print(
                "AI prediction error:",
                error
            )

            prediction = risk_level


    # ========================================================
    # BUILD RISK FACTORS
    # ========================================================

    risk_factors = build_risk_factors(

        effective_login_events,

        effective_file_events,

        effective_usb_events,

        effective_failed_logins,

        suspicious_deletions,

        suspicious_renames

    )


    # ========================================================
    # MERGE ACTIVITIES
    # ========================================================

    all_activities = []


    all_activities.extend(
        live_activities
    )


    all_activities.extend(
        db_activities
    )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_activities = []

    seen = set()


    for item in all_activities:

        key = (

            str(
                item.get(
                    "time",
                    ""
                )
            ),

            str(
                item.get(
                    "activity",
                    ""
                )
            )

        )


        if key not in seen:

            seen.add(key)

            unique_activities.append(
                item
            )


    # ========================================================
    # SORT NEWEST FIRST
    # ========================================================

    unique_activities.sort(

        key=lambda item:
            str(
                item.get(
                    "time",
                    ""
                )
            ),

        reverse=True

    )


    recent_activities = (
        unique_activities[:20]
    )


    # ========================================================
    # EMPLOYEE DATA
    # ========================================================

    employee_data = {

        "name":
            employee_info["name"],

        "department":
            employee_info["department"],

        "role":
            employee_info["role"],

        "login_hour":
            current_hour,

        "files_opened":
            effective_file_events,

        "usb_used":
            effective_usb_events,

        "failed_logins":
            effective_failed_logins

    }


    # ========================================================
    # TOTAL EVENTS
    # ========================================================

    total_events = (

        effective_login_events

        +

        effective_file_events

        +

        effective_usb_events

        +

        effective_failed_logins

    )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "login_events":
            effective_login_events,

        "file_events":
            effective_file_events,

        "usb_events":
            effective_usb_events,

        "failed_logins":
            effective_failed_logins,

        "total_events":
            total_events,

        "prediction":
            prediction,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "employee":
            employee_data,

        "activities":
            recent_activities,

        "risk_factors":
            risk_factors,

        "suspicious_event_count":
            (
                suspicious_deletions
                +
                suspicious_renames
            ),

        "suspicious_events": {

            "deletions":
                suspicious_deletions,

            "renames":
                suspicious_renames,

            "total":
                (
                    suspicious_deletions
                    +
                    suspicious_renames
                )

        },

        "monitoring": {

            "file_monitoring":
                True,

            "usb_monitoring":
                True,

            "login_monitoring":
                True

        }

    }


# ============================================================
# RISK RANKING
# ============================================================

@router.get("/risk-ranking")
def risk_ranking():

    employees = []


    try:

        # ----------------------------------------------------
        # FIRST: GET CURRENT LIVE RISK
        # ----------------------------------------------------

        dashboard_data = dashboard()


        current_employee = (
            dashboard_data["employee"]
        )


        current_name = (
            current_employee["name"]
        )


        current_department = (
            current_employee["department"]
        )


        current_risk = int(
            dashboard_data["risk_score"]
        )


        current_status = (
            dashboard_data["risk_level"]
        )


        # ----------------------------------------------------
        # DATABASE EMPLOYEES
        # ----------------------------------------------------

        with engine.connect() as connection:

            result = connection.execute(

                text("""
                    SELECT
                        employee_id,
                        total_score,
                        risk_level,
                        created_at
                    FROM risk_scores
                    ORDER BY
                        total_score DESC,
                        created_at DESC
                """)

            )


            seen = set()


            for row in result:

                employee_id = (
                    row.employee_id
                )


                if employee_id in seen:
                    continue


                seen.add(
                    employee_id
                )


                employee_info = (
                    EMPLOYEE_INFO.get(

                        employee_id,

                        {
                            "name":
                                employee_id,

                            "department":
                                "Unknown",

                            "role":
                                "Unknown"
                        }

                    )
                )


                # ------------------------------------------------
                # CURRENTLY MONITORED EMPLOYEE
                # ALWAYS USE LIVE SCORE
                # ------------------------------------------------

                if (
                    employee_info["name"]
                    == current_name
                ):

                    employees.append({

                        "name":
                            current_name,

                        "department":
                            current_department,

                        "risk":
                            current_risk,

                        "status":
                            current_status

                    })

                else:

                    employees.append({

                        "name":
                            employee_info["name"],

                        "department":
                            employee_info["department"],

                        "risk":
                            int(
                                row.total_score
                                or 0
                            ),

                        "status":
                            row.risk_level

                    })


        # ----------------------------------------------------
        # ENSURE LIVE EMPLOYEE EXISTS
        # ----------------------------------------------------

        current_exists = any(

            employee["name"]
            == current_name

            for employee in employees

        )


        if not current_exists:

            employees.append({

                "name":
                    current_name,

                "department":
                    current_department,

                "risk":
                    current_risk,

                "status":
                    current_status

            })


        # ----------------------------------------------------
        # SORT BY RISK
        # ----------------------------------------------------

        employees.sort(

            key=lambda employee:
                employee["risk"],

            reverse=True

        )


        return employees


    except Exception as error:

        print(
            "Risk ranking error:",
            error
        )


        # ----------------------------------------------------
        # SAFE FALLBACK
        # ----------------------------------------------------

        try:

            dashboard_data = dashboard()


            return [

                {

                    "name":
                        dashboard_data[
                            "employee"
                        ]["name"],

                    "department":
                        dashboard_data[
                            "employee"
                        ]["department"],

                    "risk":
                        dashboard_data[
                            "risk_score"
                        ],

                    "status":
                        dashboard_data[
                            "risk_level"
                        ]

                }

            ]


        except Exception as fallback_error:

            print(
                "Risk ranking fallback error:",
                fallback_error
            )

            return []