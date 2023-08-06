import time
from plyer import notification

if __name__ == "__main__":
        notification.notify(
            title = "Title for notification",
            message = "This is a message space. Here you can send any message or notification which you want to send.",
            timeout = 3
        )

def mt_push_notification(title, message,timeout):
    return (notification.notify
            (title = title,
            message = message,
            timeout = timeout)
        )