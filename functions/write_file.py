import os
from pathlib import Path

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