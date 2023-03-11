from desktop_notifier import DesktopNotifier

notifier = DesktopNotifier()

def send_notification(message: str) -> None:
    notifier.send_sync(title="Timekeeper", message=message, sound=True)

