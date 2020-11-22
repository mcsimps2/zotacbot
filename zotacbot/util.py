import os

import psutil


def _alert_mac(msg):
    os.system(f"say {msg}")


def _alert_win(msg):
    import winsound

    print(f"ALERT: {msg}")
    winsound.Beep(2000, 1000)


def _alert_linux(msg):
    print(f"ALERT: {msg}")
    print("\a")


def alert(msg):
    if psutil.WINDOWS:
        return _alert_win(msg)
    elif psutil.MACOS:
        return _alert_mac(msg)
    else:
        return _alert_linux(msg)
