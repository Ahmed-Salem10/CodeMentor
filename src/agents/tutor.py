from pathlib import Path

from src.state import State
from src.llm import chat


PROMPT = (
    Path(__file__).resolve().parents[2] / "prompts" / "tutor.md"
).read_text(encoding="utf-8")


def tutor(state: State):
    user_request = state["user_request"]

    response = chat([
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": user_request},
    ])

    return {"tutor_result": response}