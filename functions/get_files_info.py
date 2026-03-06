import os
from config import working_directory

def get_files_info(directory: str ="."):
    """
    Lists files and directories inside a specified directory within the
    working directory.

    The function resolves the absolute path of the requested directory and
    verifies that it resides within the provided working directory to prevent
    path traversal. It then returns basic metadata for each entry in the
    directory, including file size and whether the entry is a directory.

    Args:
        directory (str, optional): Relative path to the directory whose
            contents should be listed. Defaults to the working directory (".").

    Returns:
        str: A formatted string containing one line per directory entry in the
        format `- <name>: file_size=<bytes> is_dir=<bool>`. Returns an error
        message if the requested directory is outside the working directory.
    """
    abs_wd = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_wd):
        return f"Error: {directory} is not in the working directory"

    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        final_response += f"- {content}: file_size={size} is_dir={is_dir}\n"

    return final_response
