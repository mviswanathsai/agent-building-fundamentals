import os
from config import working_directory

def get_file_content(file_path: str) -> str:
    """
    Reads and returns the contents of a file within a specified working directory.

    The function resolves the absolute path of the target file and ensures it
    resides within the provided working directory to prevent path traversal.
    It then verifies that the path exists and refers to a regular file before
    reading its contents.

    Args:
        file_path (str): Relative path to the file whose contents should be
            retrieved.

    Returns:
        str: The full contents of the file as a string. Returns an error message
        if the file is outside the working directory, does not exist, is not a
        regular file, or if an exception occurs during file reading.
    """
    abs_wd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_wd):
        return f"Error: {file_path} does not exist inside the working directory"
    if not os.path.exists(abs_file_path):
        return f"Error: {file_path} does not exist"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read()
    except Exception as e:
        return f"Exception reading file {file_path}: {e}"


    return file_content_string


