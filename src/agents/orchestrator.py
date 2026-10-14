from src.state import RoutingDecision, State
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Send

base_llm=ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",temperature=0,max_retries=5)

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite",temperature=0,reasoning_effort="low",max_retries=5)

router=llm.with_structured_output(RoutingDecision,method="json_schema")


def orchestrator(state: State):
    user_request = state["user_request"]
    tutor_result = state.get("tutor_result", "")
    debugger_result = state.get("debugger_result", "")
    reviewer_result = state.get("reviewer_result", "")
    evaluator_result = state.get("evaluator_result", "")
    final_context = state.get("final_context", "")

    prompt = f"""
You are the Orchestrator of CodeMentor, a multi-agent system that teaches programming to beginners.
Your ONLY job is to decide which specialist agents should handle the student's request next.
You do NOT answer the student yourself.

## Available agents
- tutor: explains programming concepts simply, with examples, at a beginner level.
- debugger: explains error messages / tracebacks and gives step-by-step hints to fix the bug (not the full solution).
- reviewer: reviews the student's code for style, readability, performance and best practices, and explains why.
- evaluator: runs the student's code against tests and gives a grade with feedback.

## Student request
{user_request}

## Work already done by agents (empty means the agent has not run yet)
- tutor result: {tutor_result or "NOT RUN"}
- debugger result: {debugger_result or "NOT RUN"}
- reviewer result: {reviewer_result or "NOT RUN"}
- evaluator result: {evaluator_result or "NOT RUN"}

## Extra context
{final_context or "None"}

## Routing rules
1. Concept question ("what is a loop?", "explain recursion") -> ["tutor"].
2. The request contains an error message or says the code is not working -> ["debugger"].
3. The student asks for feedback or improvements on working code -> ["reviewer"].
4. The student submits a solution to an exercise, or asks to test or grade the code -> ["evaluator"].
5. Combine agents only when the request clearly needs more than one.
   Example: "explain this code and tell me what's wrong" -> ["tutor", "debugger"].
6. Never route to an agent that already has a result, unless the request needs new work from it.
7. If the request is already fully covered by the existing results, return an empty list [].
8. If the request is unclear or is a greeting or small talk, return ["tutor"].
9. Order matters: put the agents in the order they should run.

## Output
Return only the routing decision as structured output (next_agent), with no extra text.
The student may write in Arabic or English; understand both.
"""
    
    decision = router.invoke(prompt)

    return {"next_agent": [decision.next_agent]}

AGENTS=["tutor","debugger","reviewer","evaluator"]

def route_next_agent(state:State):
    agents=[a for a in state.get("next_agent",[]) if a in AGENTS]
    if not agents:
        return "final"

    return[Send(agent,state) for agent in agents]