from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    query: str
    messages: Annotated[List[dict], operator.add]
    # Specialized Data Slots
    market_data: dict
    exim_data: dict
    patent_data: List[dict]
    clinical_data: List[dict]
    internal_data: str
    web_data: str
    final_report_path: str
    next_step: str  # Used by Master to route
