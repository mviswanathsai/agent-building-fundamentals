import os
from config import working_directory

def write_file(file_path: str, file_content_string: str):
    """
    Creates and writes content to a file inside a specified working directory.

    The function ensures the target file resides within the provided working
    directory to prevent path traversal. It also checks that the file does not
    already exist. Parent directories are created if necessary before writing
    the provided content to the file.

    Args:
        file_path (str): Relative path of the file to create within the working directory.
        file_content_string (str): Text content to write into the file.

    Returns:
        str: A success message if the file is written successfully, or an error
        message if the file already exists, violates the working directory
        constraint, or if an exception occurs during directory creation or
        file writing.
    """
    abs_wd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_wd):
        return f"Error: {file_path} does not exist inside the working directory"
    if os.path.exists(abs_file_path) and os.path.isfile(abs_file_path):
        return f"Error: {file_path} file already exists"

    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    except Exception as e:
        return f"Exception creating parent directories for file {file_path}: {e}"

    try:
        with open(abs_file_path, "w") as f:
            file_content_string = f.write(file_content_string)
    except Exception as e:
        return f"Exception writing file {abs_file_path}: {e}"

    return f"Successfuly wrote to {file_path}"


