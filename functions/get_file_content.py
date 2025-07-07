import os
from pathlib import Path

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