import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_files",
    description="Tests if the target is a Python file and run it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Array of aditional arguments to be passed on opening file",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        file_exist = os.path.isfile(target_file)
        if not file_exist:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_directory,
            timeout=30,
            text=True,
        )

        return_string = ""
        if completed_process.returncode:
            return_string = f"Process exited with code {completed_process.returncode}"

        if not completed_process.stderr and not completed_process.stdout:
            return_string += "No output produced"
        else:
            if completed_process.stdout:
                return_string += f"STDOUT: {completed_process.stdout}"
            if completed_process.stderr:
                return_string += f"STDERR: {completed_process.stderr}"

        return return_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
