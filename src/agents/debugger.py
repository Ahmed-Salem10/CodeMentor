from pathlib import Path
from src.llm import chat 
from src.state import State

PROMPT = (
    Path(__file__).resolve().parents[2] / "prompts" / "debugger.md"
).read_text(encoding="utf-8")

def debugger(state:State):
    user_request=state["user_request"]

    response=chat([
        {"role":"system","content":PROMPT},
        {"role":"user","content":user_request}
    ])

    return {"debugger_result":response}