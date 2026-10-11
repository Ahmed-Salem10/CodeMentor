from typing import List,Literal,TypedDict
from pydantic import BaseModel,Filed
class RoutingDecision(BaseModel):
    next_agent:List[Literal["tutor","debugger","evaluator","reviewer"]]=Filed(...,desciption="the next agent to the route the query, it can be one or more of :'tutor','reviewer','evaluator','debugger'")

class State(TypedDict):
    user_request:str
    next_agent:list[str]
    
    tutor_result:str
    debugger_result:str
    reviewer_result:str
    evaluator_result:str

    final_context:str
    response:str

