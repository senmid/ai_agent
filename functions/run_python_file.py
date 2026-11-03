import os
import subprocess
import sys


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory, capturing stdout and stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "List of arguments to pass to the Python file",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
    },
}


def run_python_file(
    working_dir: str, file_path: str, args: list[str] | None = None
) -> str:
    path = os.path.abspath(working_dir)
    target_dir = os.path.normpath(os.path.join(path, file_path))
    valid_path = os.path.commonpath([path, target_dir]) == path
    try:
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = [sys.executable, target_dir]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, cwd=path, text=True, capture_output=True, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
