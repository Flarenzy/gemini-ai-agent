import os

from functions._filepath_helpers import _is_path_allowed
from functions._filepath_helpers import _walk_directory


def get_files_info(
                    working_directory: str,
                    directory: str = "."
                    ) -> str:
    """
    Returns a string ,or a error message as a string, containing the
    contents of a directory relative to the working directory.
    Each line in the string is a file in the directory and contains info lie
    file_size in bytes and if the file is a dir or not.

    Args:
        working_directory(str): Path of the current working directory
        directory(str): The dircetory to list the content's of relative to the
                        working directory

    Returns:
        str: String containing the name, size and is_dir for all
             files in a directory or a erorr message prefixed with 'Error:'.

    Example:
        res = get_files_info('calculator', '.')\n
        print(res)\n
        Result for current directory:\n
         - tests.py: file_size=1343 bytes, is_dir=False
         - main.py: file_size=576 bytes, is_dir=False
         - pkg: file_size=192 bytes, is_dir=True
    """
    try:
        full_path = os.path.join(working_directory, directory)
        file_list: list[str] = _walk_directory(working_directory)
        if not _is_path_allowed(directory, working_directory, file_list):
            return (
                    f"Result for '{directory}' directory:\n"
                    f"    Error: Cannot list '{directory}' as it "
                    f"is outside the permitted working directory"
                    )
        if not os.path.isdir(full_path):
            return f"    Error: '{directory}' is not a directory"

        dir_contents = os.listdir(full_path)
        if directory == ".":
            files_info = "Result for current directory:\n"
        else:
            files_info = f"Result for '{directory}' directory:\n"

        for dir_file in dir_contents:
            dir_file_path = os.path.join(full_path, dir_file)
            files_info += f" - {dir_file}: "
            file_size = os.path.getsize(dir_file_path)
            files_info += f"file_size={file_size} bytes, "
            is_dir = os.path.isdir(dir_file_path)
            files_info += f"is_dir={is_dir}\n"
        return files_info
    except Exception as e:
        return f"Error: {e}"
