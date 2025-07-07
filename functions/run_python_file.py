import os
from pathlib import Path


def run_python_file(working_directory, file_path):
    filepath = Path(os.path.join(working_directory, file_path))
    if (not os.path.abspath(filepath).endswith(file_path) and file_path != ".") or os.path.isabs(Path(file_path)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    elif not filepath.is_file():
        return f'Error: File "{file_path}" not found.'
    elif not file_path.endswith(".py"):
        f'Error: "{file_path}" is not a Python file.'