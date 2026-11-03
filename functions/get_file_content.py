import os

from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content of a specified file relative to the working directory, providing up to {MAX_CHARS} characters of the file's content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to retrieve content from, relative to the working directory",
                },
            },
        },
    },
}


def get_file_content(working_dir: str, file_path: str) -> str:
    working_path = os.path.abspath(working_dir)
    target_path = os.path.normpath(os.path.join(working_path, file_path))
    valid_path = os.path.commonpath(
        [working_path, target_path]) == working_path
    try:
        if not valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {e}'
