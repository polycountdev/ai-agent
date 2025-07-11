import os
from pathlib import Path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes provided content to a specified file; creating a new file if one doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to a given file."
            )
        },
    ),
)

def write_file(working_directory, file, content):
    filepath = Path(os.path.join(working_directory, file))
    if (not os.path.abspath(filepath).endswith(file) and file != ".") or os.path.isabs(Path(file)):
        return f'Error: Cannot write to "{file}" as it is outside the permitted working directory'
    elif filepath.is_file():
        f = open(filepath, "w")
        f.write(content)
        f.close()
    elif not filepath.is_file():
        f = open(filepath, "w+")
        f.write(content)
        f.close()

    return f'Successfully wrote to "{file}" ({len(content)} characters written)'