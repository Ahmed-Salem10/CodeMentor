import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_NAME = "poolside/laguna-s-2.1:free"


def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Check your .env file."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def chat(messages: list[dict], temperature: float = 0.2) -> str:
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("The model returned an empty response.")

    return content.strip()