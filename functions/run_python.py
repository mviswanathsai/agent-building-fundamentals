import os
import subprocess
from config import working_directory

def run_python(file_path: str, args:str):
    """
    Executes a Python file located inside a specified working directory.

    The function validates that the target file exists, is a Python file,
    and resides within the provided working directory to prevent path
    traversal. It then runs the file using `python3`, passing any provided
    arguments, and captures both stdout and stderr.

    Args:
        file_path (str): Relative path to the Python file to execute.
        args (str): Space-separated string of arguments to pass to the script.

    Returns:
        str: A formatted string containing the script's stdout and stderr
        output. If the process exits with a non-zero return code, the error
        code is included. Returns an error message string if validation fails
        or if an exception occurs during execution.
    """
    abs_wd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_wd):
        return f"Error: {file_path} does not exist inside the working directory"
    if not os.path.exists(abs_file_path):
        return f"Error: {file_path} file already exists"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a python file"

    final_args =["python3", file_path].extend(args.split())
    try:
        output = subprocess.run(final_args, cwd=abs_wd, timeout=30, capture_output=True)
        output_string = f"""Output from running {file_path}:
            STDOUT: {output.stdout}
            STDERR: {output.stderr}
            """
        if output.returncode != 0:
            output_string += f"Error: Process exited with code {output.returncode}"
        if output.stdout == "" and output.stderr == "":
            output_string += "No output produced\n"
    except Exception as e:
        return f"Exception running python file {file_path}: {e}"

    return output_string




