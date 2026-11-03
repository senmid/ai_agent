from call_function import available_functions, call_function
from openai import OpenAI


def generate_content(client: OpenAI, messages: list[dict], verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    if response.usage is None:
        raise RuntimeError("Usage is not available")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise RuntimeError("Result is empty")
            if verbose:
                print(f"-> {result_message['content']}")
        return None

    return f"Final response:\n{message.content}"
