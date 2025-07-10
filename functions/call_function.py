from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from google.genai import types


def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function: {function_call_part.name}")

    function_result = ""
    try:
        match function_call_part.name:
            case "write_file":
                function_result = write_file("./calculator", **function_call_part.args)
            case "get_file_content":
                function_result = get_file_content(
                    "./calculator", **function_call_part.args
                )
            case "get_files_info":
                function_result = get_files_info(
                    "./calculator", **function_call_part.args
                )
            case "run_python_file":
                function_result = run_python_file(
                    "./calculator", **function_call_part.args
                )
            case _:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={
                                "error": f"Unknown function: {function_call_part.name}"
                            },
                        )
                    ],
                )
    except Exception as e:
        print(e)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )
