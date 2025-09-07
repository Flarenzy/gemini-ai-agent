import os


from functions._filepath_helpers import _is_path_allowed
from functions._filepath_helpers import _walk_directory
from functions.config import FILE_CHAR_LIMIT


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Returns a string ,or a error message as a string, containing the
    contents of a regular file inside the working directory.

    Args:
        working_directory(str): Path of the current working directory
        file_path(str): Path to the file from which to read the content

    Returns:
        str: File content from the specified file or an error message
             with a prefix 'Error:'
    """
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return (
                    "Error: File not found or is not a "
                    f"regular file: '{file_path}'"
                    )
        file_list = _walk_directory(working_directory)
        if not _is_path_allowed(file_path, working_directory, file_list):
            return (
                    f"Error: Cannot read '{file_path}' as it is outside the"
                    " permitted working directory"
                    )

        with open(full_path, "r") as f:
            content = f.read(FILE_CHAR_LIMIT)

        truncated = len(content) == FILE_CHAR_LIMIT and f.read(1) != ""
        if truncated:
            content += (f"[...File '{file_path}' "
                        "truncated at 10000 characters]")
        return content
    except Exception as e:
        return f"Error: {e}"
