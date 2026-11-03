import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from generate_content import generate_content
from prompt import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument(
        "user_prompt",
        type=str,
        help="The user prompt to send to the chatbot",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        final = generate_content(client, messages, args.verbose)
        if final is not None:
            print(final)
            break
    else:
        raise RuntimeError("Max iterations reached without a final response")


if __name__ == "__main__":
    main()
