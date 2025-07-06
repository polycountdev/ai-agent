import os
from pathlib import Path

def get_files_info(working_directory, directory=None):
    filepath = Path(os.path.join(working_directory, directory))
    print(f"filepath is: {os.path.abspath(filepath)}")
    if not os.path.abspath(filepath).endswith(directory) and directory != ".":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not filepath.is_dir():
        return f'Error: "{filepath}" is not a directory'
    
    dir_contents = os.listdir(filepath)
    print(f"dir contents: {dir_contents}")

    return_str = ""
    for item in dir_contents:
        current_path = Path(os.path.join(filepath, item))
        return_str = return_str + f"- {item}: file_size={os.path.getsize(current_path)} bytes, is_dir={current_path.is_dir()}\n"
    
    return return_str