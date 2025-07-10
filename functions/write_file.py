import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.join(abs_working_dir, file_path)
    if not target_path.startswith(abs_working_dir):
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"
    elif os.path.isdir(target_path):
        return f"Error: {file_path} is a directory, not a file"

    try:
        curr_file = open(target_path, "w")
        curr_file.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    except Exception as error:
        return f"Error: writing to file: {error}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Either creates or updates a file with the content passed within the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be used to update the file, specified by the directory and file path.",
            ),
        },
    ),
)
