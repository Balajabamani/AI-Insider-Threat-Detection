import win32com.client

print("=" * 60)
print("Listening for Windows USB Events...")
print("Insert or Remove a USB Device")
print("=" * 60)

watcher = win32com.client.GetObject(
    "winmgmts:"
).ExecNotificationQuery(
    """
    SELECT * FROM Win32_VolumeChangeEvent
    """
)

while True:

    event = watcher.NextEvent()

    if event.EventType == 2:
        print(f"\nUSB CONNECTED : {event.DriveName}")

    elif event.EventType == 3:
        print(f"\nUSB REMOVED : {event.DriveName}")