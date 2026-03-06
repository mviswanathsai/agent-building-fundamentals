import os
from config import working_directory

def get_files_info(directory: str ="."):
    """
    Lists files and directories within a specified directory under the
    configured working directory.

    The function resolves the provided relative path against the configured
    `working_directory` and ensures the resolved path remains within that
    directory to prevent path traversal. It then lists the directory contents
    and returns a formatted summary separating files and directories.

    Each entry includes the item name and its size in bytes.

    Args:
        directory (str, optional): Relative path of the directory to inspect,
            resolved relative to the configured working directory. Defaults
            to the working directory itself (".").

    Returns:
        str: A formatted string describing the directory contents, structured
        with separate sections for files and directories. Each entry is
        formatted as:

            - <name>: size=<bytes>

        Returns an error message if:
        - The resolved path is outside the working directory.
        - The specified directory does not exist.
    """
    abs_wd = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_wd):
        return f"Error: {directory} is not in the working directory"

    if not os.path.exists(abs_directory):
        return f"Error: {directory} does not exist. Check the directory structure and ensure the path is correct."

    files = ""
    dirs = ""
    contents = sorted(os.listdir(abs_directory))
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        if is_dir:
            dirs  += f"- {content}: size={size}\n"
        else:
            files  += f"- {content}: size={size}\n"

    return f"Files:\n{files}\nDirectories:\n{dirs}"
