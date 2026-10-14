from typing import List,Literal,TypedDict,Annotated
from pydantic import BaseModel,Field
from langgraph.graph.message import add_messages

class RoutingDecision(BaseModel):
    next_agent:List[Literal["tutor","debugger","evaluator","reviewer"]]=Field(...,desciption="the next agent to the route the query, it can be one or more of :'tutor','reviewer','evaluator','debugger'")


class State(TypedDict):
    user_request:str
    next_agent:list[str]
    messages:Annotated[list[dict],add_messages]
    
    tutor_result:str
    debugger_result:str
    reviewer_result:str
    evaluator_result:str

    final_context:str
    response:str

