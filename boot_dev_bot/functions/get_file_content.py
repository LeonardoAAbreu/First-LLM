import os

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Tests if the target is a file and return its contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        file_exist = os.path.isfile(target_file)

        if not valid_target_file:
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
        if not file_exist:
            return f"Error: File not found or is not a regular file: '{file_path}'"

        with open(target_file, "r") as f:
            file_readings = f.read(10000)
            if f.read(1):
                file_readings += (
                    f"[...File '{file_path}' truncated at {10000} characters"
                )
        return file_readings

    except Exception as e:
        return f"Error: {e}"
