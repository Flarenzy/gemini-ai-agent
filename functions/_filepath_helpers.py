from pathlib import Path


def _is_path_allowed(
                    file_path: str,
                    work_dir: str,
                    ) -> bool:
    """
    Check if file_path is inside work_dir.

    Args:
        file_path (str): Absolute or relative path to check.
        work_dir (str): The root working directory.
    Returns:
        bool: True if file_path is within work_dir
    """
    workdir = Path(work_dir).resolve()
    target = (workdir / file_path).resolve()

    try:
        target.relative_to(workdir)   # raises ValueError if outside
        return True
    except ValueError:
        return False
