import contextlib
import os
import signal
import subprocess

from functions._filepath_helpers import _is_path_allowed


class TimeoutException(Exception):
    pass


def _timeout_handler(signum: int, frame):
    raise TimeoutException("Operation timeout")


@contextlib.contextmanager
def timeout(seconds: int):
    old_hanlder = signal.getsignal(signalnum=signal.SIGALRM)
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_hanlder)


def run_python_file(working_directory: str,
                    file_path: str,
                    args: list[str] | None = None) -> str:
    try:
        if not _is_path_allowed(file_path, working_directory):
            return (f'Error: Cannot execute "{file_path}" as it '
                    'is outside the permitted working directory')
        full_path = os.path.join(working_directory, file_path)
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith(".py"):
            return f"Error: '{file_path}' is not a Python file."
        cmd = ["python", file_path]
        if args is not None:
            cmd += args
        with timeout(30):
            result = subprocess.run(cmd,
                                    capture_output=True,
                                    text=True,
                                    check=True,
                                    cwd=working_directory)
            if result.returncode != 0:
                return f"Process exited with code {result.returncode}"
            if not result.stdout and not result.stderr:
                return "No output produced"
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
