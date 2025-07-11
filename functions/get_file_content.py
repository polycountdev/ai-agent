import os
from pathlib import Path
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read the contents of, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    filepath = Path(os.path.join(working_directory, file_path))
    if (not os.path.abspath(filepath).endswith(file_path) and file_path != ".") or os.path.isabs(Path(file_path)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    elif not filepath.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    file_open = open(filepath)
    file_read = file_open.read()
    file_open.close()

    if len(str(file_read)) < 10000:
        return file_read
    else: 
        return file_read[:10000] + (f'[...File "{filepath}" truncated at 10000 characters]')