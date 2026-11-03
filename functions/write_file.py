import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory, ensuring the file is created and the content is saved",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
        },
    },
}


def write_file(working_dir: str, file_path: str, content: str) -> str:
    path = os.path.abspath(working_dir)
    target_dir = os.path.normpath(os.path.join(path, file_path))
    valid_path = os.path.commonpath([path, target_dir]) == path
    try:
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_dir)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
