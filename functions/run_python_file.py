import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.join(abs_working_dir, file_path)
    file_path_arr = file_path.split("/")
    if not target_path.startswith(abs_working_dir) or len(file_path_arr) > 1:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found'
    elif not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        result = subprocess.run(
            ["python", target_path], timeout=30000, capture_output=True, text=True
        )
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if result.stdout is None or result.stderr is None:
            return "No output produced"
    except Exception as error:
        return f"Error: executing Python file: {error}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file within the directory passed using the system's python interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written to, relative to the working directory.",
            )
        },
    ),
)
