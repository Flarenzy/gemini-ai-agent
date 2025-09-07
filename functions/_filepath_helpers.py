import os


def _walk_directory(root_dir: str) -> list[str]:
    """
    Walks the root directory and returns a list of relative paths
    to files and directories inside it (relative to root_dir).

    Args:
        root_dir (str): The root directory from where to start the walk.
    Returns:
        list[str]: List of files and directories (relative to root_dir).
                   If root_dir is not a directory, returns an empty list.
    """
    if not os.path.isdir(root_dir):
        return []

    file_list: list[str] = []
    for root, dir_names, file_names in os.walk(root_dir):
        for name in dir_names + file_names:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, start=root_dir)
            if "__pycache__" not in rel_path.split(os.sep):
                file_list.append(rel_path)
    return file_list


def _is_path_allowed(
                    file_path: str,
                    work_dir: str,
                    allowed_list: list[str]
                    ) -> bool:
    """
    Check if file_path is inside work_dir and part of allowed_list.

    Args:
        file_path (str): Absolute or relative path to check.
        work_dir (str): The root working directory.
        allowed_list (list[str]): List of relative paths under work_dir.
    Returns:
        bool: True if file_path is within work_dir and in allowed_list.
    """
    abs_work_dir = os.path.abspath(work_dir)
    abs_file = os.path.abspath(os.path.join(abs_work_dir, file_path))

    # Ensure file is inside the working directory
    try:
        rel_path = os.path.relpath(abs_file, start=abs_work_dir)
    except ValueError:
        # Different drive on Windows
        return False

    if rel_path.startswith(".."):
        return False

    if rel_path == ".":
        return True

    return rel_path in allowed_list
