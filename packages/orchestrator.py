import os
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

# Import State
from packages.state import AgentState

# Import Agents
from packages.agents.patent_agent import patent_agent_node
from packages.agents.clinical_agent import clinical_agent_node
from packages.agents.market_agent import market_agent_node
from packages.agents.exim_agent import exim_agent_node
from packages.agents.web_agent import web_agent_node
from packages.agents.internal_agent import internal_agent_node
from packages.agents.report_agent import report_agent_node

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

def master_agent_node(state: AgentState):
    """
    The Brain: Decides which agent to call next based on what data is missing.
    """
    # Check what data we already have
    has_market = state.get("market_data") is not None
    has_patent = state.get("patent_data") is not None
    has_clinical = state.get("clinical_data") is not None
    has_web = state.get("web_data") is not None
    has_report = state.get("final_report_path") is not None

    # Routing Logic (Fixed Sequence for Stability, or LLM driven)
    # For robustness, we enforce a logical flow:
    if not has_market:
        return {"next_step": "market_agent"}
    elif not has_patent:
        return {"next_step": "patent_agent"}
    elif not has_clinical:
        return {"next_step": "clinical_agent"}
    elif not has_web:
        return {"next_step": "web_agent"}
    elif not has_report:
        return {"next_step": "report_agent"}
    else:
        return {"next_step": "end"}

def router(state: AgentState):
    return state["next_step"]

# Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("master", master_agent_node)
workflow.add_node("market_agent", market_agent_node)
workflow.add_node("patent_agent", patent_agent_node)
workflow.add_node("clinical_agent", clinical_agent_node)
workflow.add_node("web_agent", web_agent_node)
# (Add EXIM and Internal if needed, keeping it to 5 core for brevity, but pattern is same)
workflow.add_node("report_agent", report_agent_node)

# Set Entry
workflow.set_entry_point("master")

# Edges (Star Graph)
workflow.add_conditional_edges(
    "master",
    router,
    {
        "market_agent": "market_agent",
        "patent_agent": "patent_agent",
        "clinical_agent": "clinical_agent",
        "web_agent": "web_agent",
        "report_agent": "report_agent",
        "end": END
    }
)

# Return to Master after each agent work
workflow.add_edge("market_agent", "master")
workflow.add_edge("patent_agent", "master")
workflow.add_edge("clinical_agent", "master")
workflow.add_edge("web_agent", "master")
workflow.add_edge("report_agent", "master")

app_graph = workflow.compile()
