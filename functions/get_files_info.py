import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_dir: str, directory: str = ".") -> str:
    path = os.path.abspath(working_dir)
    target_dir = os.path.normpath(os.path.join(path, directory))
    valid_target_dir = os.path.commonpath([path, target_dir]) == path
    try:
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            name = os.path.basename(item_path)
            file_size = os.path.getsize(item_path)
            isdir = os.path.isdir(item_path)
            result.append(
                f'- {name}: file_size={file_size} bytes, is_dir={isdir}')
        return '\n'.join(result)
    except Exception as e:
        return f'Error: {e}'
