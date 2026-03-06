from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python

available_tools = [
            get_files_info,
            get_file_content,
            write_file,
            run_python,
            ]

available_tools_map = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python": run_python,
            }
