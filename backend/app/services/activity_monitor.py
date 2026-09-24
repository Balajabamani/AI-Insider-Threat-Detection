import os
import time
import string
import threading
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ============================================================
# GLOBAL ACTIVITY STORAGE
# ============================================================

recent_activities = []

MAX_ACTIVITIES = 100

activity_counts = {
    "file": 0,
    "usb": 0,
    "login": 0,
    "failed_login": 0,
    "suspicious_file": 0
}

lock = threading.Lock()


# ============================================================
# DIRECTORIES TO IGNORE
# ============================================================

IGNORED_DIRECTORIES = {
    "$recycle.bin",
    "system volume information",

    # Windows
    "windows",
    "program files",
    "program files (x86)",
    "programdata",

    # User/application background data
    "appdata",

    # Development
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".git",

    # Temporary/cache
    "temp",
    "tmp",
    "cache",
    "caches"
}


# ============================================================
# FILES TO IGNORE
# ============================================================

IGNORED_FILE_NAMES = {
    "desktop.ini",
    "state.json",

    "cookies",
    "cookies-journal",

    "quotamanager",
    "quotamanager-journal",

    "reporting and nel",
    "reporting and nel-journal",

    "network persistent state",

    "preferences",

    "site security service state",

    "actionfxcache",

    "actionsserver"
}


# ============================================================
# FILE EXTENSIONS TO IGNORE
# ============================================================

IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",

    ".tmp",
    ".temp",

    ".etl",

    ".log",
    ".log1",
    ".log2",

    ".journal",

    ".db-wal",
    ".db-shm",

    ".crdownload",
    ".part"
}


# ============================================================
# FILE NAME PATTERNS TO IGNORE
# ============================================================

IGNORED_PATTERNS = [
    "cookies",
    "quotamanager",
    "reporting and nel",
    "network persistent state",
    "site security service state",
    "actionfxcache",
    "actionsserver",
    "webcache",
]


# ============================================================
# DUPLICATE EVENT CONTROL
# ============================================================

last_events = {}

DUPLICATE_WINDOW = 1.0


def is_duplicate_event(action, target):

    now = time.time()

    key = (
        action.upper(),
        target.lower()
    )

    with lock:

        previous_time = last_events.get(key)

        if previous_time is not None:

            if (
                now - previous_time
                < DUPLICATE_WINDOW
            ):
                return True

        last_events[key] = now

        # Keep memory under control
        if len(last_events) > 500:

            oldest = sorted(
                last_events,
                key=last_events.get
            )[:250]

            for item in oldest:

                del last_events[item]

    return False


# ============================================================
# PATH FILTER
# ============================================================

def should_ignore(path):

    try:

        normalized = os.path.abspath(
            path
        ).lower()

        file_name = os.path.basename(
            normalized
        )

        # ----------------------------------------------------
        # Windows / application directories
        # ----------------------------------------------------

        blocked_paths = [

            "\\windows\\",

            "\\program files\\",

            "\\program files (x86)\\",

            "\\programdata\\",

            "\\appdata\\",

            "\\$recycle.bin\\",

            "\\system volume information\\",

            "\\node_modules\\",

            "\\.venv\\",

            "\\venv\\",

            "\\__pycache__\\",

            "\\.git\\"
        ]

        for blocked_path in blocked_paths:

            if blocked_path in normalized:

                return True

        # ----------------------------------------------------
        # Directory-name filtering
        # ----------------------------------------------------

        parts = normalized.split(
            os.sep
        )

        for part in parts:

            if part in IGNORED_DIRECTORIES:

                return True

        # ----------------------------------------------------
        # Exact filename filtering
        # ----------------------------------------------------

        if file_name in {

            name.lower()
            for name in
            IGNORED_FILE_NAMES

        }:

            return True

        # ----------------------------------------------------
        # Extension filtering
        # ----------------------------------------------------

        for extension in IGNORED_EXTENSIONS:

            if file_name.endswith(
                extension
            ):

                return True

        # ----------------------------------------------------
        # Background application patterns
        # ----------------------------------------------------

        for pattern in IGNORED_PATTERNS:

            if pattern in file_name:

                return True

        # ----------------------------------------------------
        # Screenshot artifacts
        # ----------------------------------------------------

        if file_name.startswith(
            "screenshot "
        ):

            return True

        # ----------------------------------------------------
        # Temporary files
        # ----------------------------------------------------

        if (
            file_name.endswith(".tmp")
            or
            file_name.endswith(".temp")
        ):

            return True

        return False

    except Exception:

        return False


# ============================================================
# ADD ACTIVITY
# ============================================================

def add_activity(
    action,
    target,
    activity_type="file",
    suspicious=False
):

    if is_duplicate_event(
        action,
        target
    ):

        return

    now = datetime.now()

    activity = {

        "time":
            now.strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ),

        "activity":
            f"{action} - {target}"
    }

    with lock:

        recent_activities.insert(
            0,
            activity
        )

        del recent_activities[
            MAX_ACTIVITIES:
        ]

        if activity_type in activity_counts:

            activity_counts[
                activity_type
            ] += 1

        if suspicious:

            activity_counts[
                "suspicious_file"
            ] += 1

    print(
        "REAL-TIME ACTIVITY: "
        f"{activity['activity']} "
        f"at {activity['time']}"
    )


# ============================================================
# GET ACTIVITIES
# ============================================================

def get_activities():

    with lock:

        return recent_activities.copy()


# ============================================================
# GET COUNTS
# ============================================================

def get_activity_counts():

    with lock:

        return activity_counts.copy()


# ============================================================
# MONITOR SNAPSHOT
# ============================================================

def get_monitor_snapshot():

    with lock:

        return {

            "activities":
                recent_activities.copy(),

            "counts":
                activity_counts.copy()
        }


# ============================================================
# FILE SYSTEM HANDLER
# ============================================================

class FileActivityHandler(
    FileSystemEventHandler
):

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    def on_created(self, event):

        if event.is_directory:

            return

        if should_ignore(
            event.src_path
        ):

            return

        file_name = os.path.basename(
            event.src_path
        )

        add_activity(
            "CREATED",
            file_name,
            "file",
            False
        )

    # --------------------------------------------------------
    # MODIFY
    # --------------------------------------------------------

    def on_modified(self, event):

        if event.is_directory:

            return

        if should_ignore(
            event.src_path
        ):

            return

        file_name = os.path.basename(
            event.src_path
        )

        add_activity(
            "MODIFIED",
            file_name,
            "file",
            False
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def on_deleted(self, event):

        if event.is_directory:

            return

        if should_ignore(
            event.src_path
        ):

            return

        file_name = os.path.basename(
            event.src_path
        )

        add_activity(
            "DELETED",
            file_name,
            "file",
            True
        )

    # --------------------------------------------------------
    # RENAME
    # --------------------------------------------------------

    def on_moved(self, event):

        if event.is_directory:

            return

        if should_ignore(
            event.src_path
        ):

            return

        if should_ignore(
            event.dest_path
        ):

            return

        old_name = os.path.basename(
            event.src_path
        )

        new_name = os.path.basename(
            event.dest_path
        )

        add_activity(
            "RENAMED",
            f"{old_name} → {new_name}",
            "file",
            True
        )


# ============================================================
# FIND WINDOWS DRIVES
# ============================================================

def get_windows_drives():

    drives = []

    for letter in string.ascii_uppercase:

        drive = f"{letter}:\\"

        try:

            if os.path.exists(drive):

                drives.append(drive)

        except Exception:

            pass

    return drives


# ============================================================
# SYSTEM-WIDE FILE MONITOR
# ============================================================

def start_file_monitor():

    drives = get_windows_drives()

    print("")
    print(
        "SYSTEM FILE MONITOR INITIALIZING"
    )

    print(
        "=" * 55
    )

    if not drives:

        print(
            "No Windows drives detected."
        )

        return

    observer = Observer()

    handler = FileActivityHandler()

    # --------------------------------------------------------
    # Monitor every available drive
    # --------------------------------------------------------

    for drive in drives:

        print(
            f"Monitoring drive: {drive}"
        )

        try:

            observer.schedule(
                handler,
                drive,
                recursive=True
            )

        except Exception as error:

            print(
                f"Could not monitor "
                f"{drive}: {error}"
            )

    try:

        observer.start()

        print("")
        print(
            "SYSTEM-WIDE FILE MONITORING STARTED"
        )

        print(
            "Normal Windows/application "
            "background activity is filtered."
        )

        while True:

            time.sleep(1)

    except Exception as error:

        print(
            "File monitoring error:",
            error
        )

    finally:

        observer.stop()

        observer.join()


# ============================================================
# USB MONITOR
# ============================================================

def usb_monitor():

    try:

        import win32com.client

        locator = (
            win32com.client.Dispatch(
                "WbemScripting.SWbemLocator"
            )
        )

        service = locator.ConnectServer(
            ".",
            "root\\CIMV2"
        )

        query = service.ExecNotificationQuery(
            "SELECT * "
            "FROM Win32_VolumeChangeEvent"
        )

        print(
            "USB MONITORING STARTED"
        )

        while True:

            event = query.NextEvent()

            event_type = event.EventType

            drive_name = getattr(
                event,
                "DriveName",
                None
            )

            if not drive_name:

                drive_name = (
                    "USB Device"
                )

            # USB CONNECT
            if event_type == 2:

                add_activity(
                    "CONNECTED",
                    drive_name,
                    "usb",
                    True
                )

            # USB DISCONNECT
            elif event_type == 3:

                add_activity(
                    "DISCONNECTED",
                    drive_name,
                    "usb",
                    True
                )

    except Exception as error:

        print(
            "USB monitoring could not start:",
            error
        )


# ============================================================
# WINDOWS LOGIN MONITOR
# ============================================================

def login_monitor():

    try:

        import win32evtlog

        server = None

        log_name = "Security"

        handle = (
            win32evtlog.OpenEventLog(
                server,
                log_name
            )
        )

        print(
            "WINDOWS LOGIN MONITORING STARTED"
        )

        known_records = set()

        first_scan = True

        while True:

            try:

                events = (
                    win32evtlog.ReadEventLog(

                        handle,

                        win32evtlog.EVENTLOG_BACKWARDS_READ
                        |
                        win32evtlog.EVENTLOG_SEQUENTIAL_READ,

                        0
                    )
                )

                if events:

                    for event in events[:50]:

                        record_number = (
                            event.RecordNumber
                        )

                        if (
                            record_number
                            in known_records
                        ):

                            continue

                        known_records.add(
                            record_number
                        )

                        event_id = (
                            event.EventID
                            & 0xFFFF
                        )

                        # Ignore existing login
                        # events during startup
                        if first_scan:

                            continue

                        # 4624 = successful login
                        if event_id == 4624:

                            add_activity(
                                "LOGIN",
                                "Windows user login",
                                "login",
                                False
                            )

                        # 4625 = failed login
                        elif event_id == 4625:

                            add_activity(
                                "FAILED LOGIN",
                                "Windows authentication failure",
                                "failed_login",
                                True
                            )

                first_scan = False

                if len(
                    known_records
                ) > 1000:

                    known_records = set(
                        list(
                            known_records
                        )[-500:]
                    )

            except Exception as error:

                print(
                    "Login event read error:",
                    error
                )

            time.sleep(3)

    except Exception as error:

        print(
            "Windows login monitoring "
            "could not start:",
            error
        )


# ============================================================
# START ALL MONITORS
# ============================================================

def start_monitoring(
    monitored_folder=None
):

    print("")
    print(
        "Starting real-time "
        "system monitoring..."
    )

    # FILE MONITOR
    file_thread = threading.Thread(
        target=start_file_monitor,
        daemon=True
    )

    file_thread.start()

    # USB MONITOR
    usb_thread = threading.Thread(
        target=usb_monitor,
        daemon=True
    )

    usb_thread.start()

    # LOGIN MONITOR
    login_thread = threading.Thread(
        target=login_monitor,
        daemon=True
    )

    login_thread.start()

    print(
        "All monitoring threads started."
    )