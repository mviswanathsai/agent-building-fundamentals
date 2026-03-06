from functions.config import available_tools_map
from google.genai import types

working_dir = "calculator"

def call_function(function_name, function_args, verbose=False):

    if verbose:
        print(f"Calling function: {function_name} with args {function_args}")
    else:
        print(f"Calling function: {function_name}")

    result = ""
    tool = available_tools_map.get(function_name)
    result = tool(**function_args)

    if result == "":
        return f"Error: Unknown function: {function_name}"
    else:
        return  result


