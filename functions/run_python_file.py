import os
from pathlib import Path
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns the result.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path):

    # Convert to absolute paths and check if file_path stays within working_directory
    working_abs = os.path.abspath(working_directory)
    file_abs = Path(os.path.abspath(os.path.join(working_directory, file_path)))

    if not str(file_abs).startswith(working_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not file_abs.is_file():
        return f'Error: File "{file_path}" not found.'
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    output = subprocess.run(['python', file_path],
                            capture_output=True,
                            text=True,
                            timeout=30,
                            cwd=working_directory
                            )
    return_str = f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
    if output.returncode != 0:
        return_str = return_str + \
            f"\nProcess exited with code {output.returncode}"
    if not output.stdout and not output.stderr:
        return "No output produced."
    return return_str
