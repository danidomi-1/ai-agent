import os


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.join(abs_working_dir, file_path)
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        file_obj = open(target_path, "r")
        file_content = file_obj.read()
        file_obj.close()
        if len(file_content) > 10000:
            file_content = file_content[:10000]
        return file_content
    except Exception as e:
        return f"Error: {e}"
