import os
import time
def LogFile_path(path: str):
    """
    Creates a log file at the specified path.

    Args:
        path (str): Path pattern for the log file, which can include date and time placeholders.

    Returns:
        str: Success message if the log file is created, error message otherwise.
    """
    formatted_path = time.strftime(path, time.localtime())
    if not formatted_path.endswith('.txt'):
        return "File type must be '.txt', not anything else!"
    if os.path.exists(formatted_path):
        return f"Path '{formatted_path}' already exists!"
    else:
        os.makedirs(os.path.dirname(formatted_path), exist_ok=True)  # Yeni dizini oluştur
        with open(formatted_path, "w") as f:
            pass
        with open("PythonLogging/path.ini", "w") as f:
            f.write(formatted_path)
def log(logmsg: str):
    """
    Writes a log message to the specified log file.
    if log file unspecified, you have to use 'PythonLogging.logfile_path('yourpath')'

    Args:
        logmsg (str): Log message to be written.

    Returns:
        str: Success message if the log message is written, error message otherwise.
    """
    try:
        with open("PythonLogging/path.ini", "r") as f:
            path = f.readline().strip()
        now = time.strftime("%d.%m.%y - %H:%M:%S", time.localtime())
        with open(path, "a") as f:
            f.write(f"[{now}] {logmsg}\n")
    except FileNotFoundError:
        return "You have to select a path for logging, use PythonLogging.logfile_path('yourpath')"
