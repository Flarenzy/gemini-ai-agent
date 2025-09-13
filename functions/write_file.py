import os

from functions._filepath_helpers import _is_path_allowed


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Write the `content` into the file definied by the file_path inside of the
    working directory.

    Args:
        working_directory(str): Path of the current working directory.
        file_path(str): relative path to the file to write to inside of the
                        working directory.
        content(str): The content to be written to the file.

    Returns:
        str: String containg either an error message or success message.
    """
    try:
        if not _is_path_allowed(file_path, working_directory):
            return (
                    f"Error: Cannot write to '{file_path}' as it "
                    "is outside the permitted working directory"
                    )
        full_path = os.path.join(working_directory, file_path)
        with open(full_path, "w") as f:
            f.write(content)
        return (
                f"Successfully wrote to '{file_path}' "
                f"({len(content)} characters written)")
    except Exception as e:
        return f"Error: {e}"
