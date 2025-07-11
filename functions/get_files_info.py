import os
from pathlib import Path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    if directory:
        filepath = Path(os.path.join(working_directory, directory))
        if (not os.path.abspath(filepath).endswith(directory) and directory != ".") or os.path.isabs(Path(directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        filepath = Path(working_directory)
        
    if not filepath.is_dir():
        return f'Error: "{filepath}" is not a directory'

    dir_contents = os.listdir(filepath)

    return_str = ""
    for item in dir_contents:
        current_path = Path(os.path.join(filepath, item))
        return_str = return_str + f"- {item}: file_size={os.path.getsize(current_path)} bytes, is_dir={current_path.is_dir()}\n"

    return return_str
