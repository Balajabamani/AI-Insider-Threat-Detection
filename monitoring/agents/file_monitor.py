import os
import sys
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from sqlalchemy import text
from database.connection import engine


WATCH_FOLDER = r"E:\InsiderThreatTest"


class FileMonitor(FileSystemEventHandler):

    def save_event(self, filename, action, filepath):

        activity = {
            "employee_id": "EMP001",
            "file_name": filename,
            "action": action,
            "file_path": filepath
        }

        try:

            with engine.connect() as connection:

                connection.execute(
                    text("""
                        INSERT INTO file_activity
                        (employee_id,file_name,action,file_path)

                        VALUES
                        (:employee_id,
                         :file_name,
                         :action,
                         :file_path)
                    """),
                    activity
                )

                connection.commit()

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"{action} -> {filename}"
            )

        except Exception as e:

            print(e)

    def on_created(self, event):

        if not event.is_directory:

            self.save_event(
                os.path.basename(event.src_path),
                "CREATED",
                event.src_path
            )

    def on_deleted(self, event):

        if not event.is_directory:

            self.save_event(
                os.path.basename(event.src_path),
                "DELETED",
                event.src_path
            )

    def on_modified(self, event):

        if not event.is_directory:

            self.save_event(
                os.path.basename(event.src_path),
                "MODIFIED",
                event.src_path
            )

    def on_moved(self, event):

        if not event.is_directory:

            self.save_event(
                os.path.basename(event.dest_path),
                "RENAMED",
                event.dest_path
            )


observer = Observer()

observer.schedule(
    FileMonitor(),
    WATCH_FOLDER,
    recursive=True
)

observer.start()

print("=" * 60)
print("REAL-TIME FILE MONITOR STARTED")
print(WATCH_FOLDER)
print("=" * 60)

try:

    while True:
        pass

except KeyboardInterrupt:

    observer.stop()

observer.join()