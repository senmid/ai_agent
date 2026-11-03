# AI Agent

CLI coding agent built for the [Boot.dev](https://www.boot.dev) **Build an AI Agent** course.

It talks to an LLM through [OpenRouter](https://openrouter.ai), then uses tool calls to list files, read and write files, and run Python. Tool access is sandboxed to the `calculator/` directory.

## Requirements

- Python 3.13+
- An OpenRouter API key
- [`uv`](https://github.com/astral-sh/uv) (recommended) or a normal virtualenv

## Setup

```bash
cp .env.example .env
# Put your key in .env:
# OPENROUTER_API_KEY=your_key_here

uv sync
# or: python -m venv .venv && source .venv/bin/activate && pip install -e .
```

Never commit `.env`. Only `.env.example` belongs in the repo.

## Usage

```bash
uv run python main.py "What files are in the calculator project?"
uv run python main.py "Run calculator/main.py with 3 + 5" --verbose
```

`--verbose` prints token usage and tool call details.

The agent loops up to 20 model turns: call tools, feed results back, repeat until it returns a final answer.

## Tools

| Tool | Purpose |
|------|---------|
| `get_files_info` | List files in a directory (size + is_dir) |
| `get_file_content` | Read a file (truncated at `MAX_CHARS`) |
| `write_file` | Create or overwrite a file |
| `run_python_file` | Run a `.py` file with optional args |

All paths are relative to `calculator/`. Paths outside that sandbox are rejected.

## Project layout

```
main.py                 # CLI entrypoint
generate_content.py     # One model turn + tool dispatch
call_function.py        # Maps tool names to implementations
prompt.py               # System prompt
config.py               # Shared limits (e.g. MAX_CHARS)
functions/              # Tool schemas + implementations
calculator/             # Sandboxed workspace the agent can touch
test_*.py               # Manual smoke scripts for each tool
```

## Manual tool checks

```bash
uv run python test_get_files_info.py
uv run python test_get_file_content.py
uv run python test_write_file.py
uv run python test_run_python_file.py
```
