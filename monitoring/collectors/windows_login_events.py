import win32evtlog

SERVER = "localhost"
LOGTYPE = "Security"

print("=" * 60)
print("Listening for Windows Login Events...")
print("=" * 60)

hand = win32evtlog.OpenEventLog(SERVER, LOGTYPE)

flags = (
    win32evtlog.EVENTLOG_BACKWARDS_READ |
    win32evtlog.EVENTLOG_SEQUENTIAL_READ
)

events = win32evtlog.ReadEventLog(hand, flags, 0)

for event in events:

    if event.EventID == 4624:

        print("=" * 50)
        print("LOGIN DETECTED")
        print("Time :", event.TimeGenerated)
        print("Event ID :", event.EventID)
        print("=" * 50)