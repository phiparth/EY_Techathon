import os
import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

# Import State
from packages.state import AgentState

# Import ALL 7 Agents
from packages.agents.patent_agent import patent_agent_node
from packages.agents.clinical_agent import clinical_agent_node
from packages.agents.market_agent import market_agent_node
from packages.agents.exim_agent import exim_agent_node
from packages.agents.web_agent import web_agent_node
from packages.agents.internal_agent import internal_agent_node
from packages.agents.report_agent import report_agent_node

# --- 1. ROBUST API KEY FETCHING (Sherlock Fix) ---
api_key = os.getenv("GOOGLE_API_KEY")

# If not in OS (local), check Streamlit Secrets (cloud)
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

# If still missing, raise a clear error
if not api_key:
    raise ValueError("FATAL ERROR: GOOGLE_API_KEY is missing. Add it to .env (local) or Streamlit Secrets (cloud).")

# Initialize LLM with the explicit key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", 
    temperature=0,
    google_api_key=api_key
)

# --- 2. MASTER AGENT LOGIC (The Brain) ---
def master_agent_node(state: AgentState):
    """
    The Brain: Decides which agent to call next based on what data is missing.
    """
    # Check what data we already have
    has_market = state.get("market_data") is not None
    has_patent = state.get("patent_data") is not None
    has_clinical = state.get("clinical_data") is not None
    has_exim = state.get("exim_data") is not None      # Added
    has_internal = state.get("internal_data") is not None # Added
    has_web = state.get("web_data") is not None
    has_report = state.get("final_report_path") is not None

    # Routing Logic (Sequential flow for stability)
    if not has_market:
        return {"next_step": "market_agent"}
    elif not has_patent:
        return {"next_step": "patent_agent"}
    elif not has_clinical:
        return {"next_step": "clinical_agent"}
    elif not has_exim:
        return {"next_step": "exim_agent"}     # Added Route
    elif not has_internal:
        return {"next_step": "internal_agent"} # Added Route
    elif not has_web:
        return {"next_step": "web_agent"}
    elif not has_report:
        return {"next_step": "report_agent"}
    else:
        return {"next_step": "end"}

def router(state: AgentState):
    return state["next_step"]

# --- 3. BUILD GRAPH ---
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("master", master_agent_node)
workflow.add_node("market_agent", market_agent_node)
workflow.add_node("patent_agent", patent_agent_node)
workflow.add_node("clinical_agent", clinical_agent_node)
workflow.add_node("exim_agent", exim_agent_node)         # Added Node
workflow.add_node("internal_agent", internal_agent_node) # Added Node
workflow.add_node("web_agent", web_agent_node)
workflow.add_node("report_agent", report_agent_node)

# Set Entry
workflow.set_entry_point("master")

# Edges (Star Graph Logic)
workflow.add_conditional_edges(
    "master",
    router,
    {
        "market_agent": "market_agent",
        "patent_agent": "patent_agent",
        "clinical_agent": "clinical_agent",
        "exim_agent": "exim_agent",          # Added Edge
        "internal_agent": "internal_agent",  # Added Edge
        "web_agent": "web_agent",
        "report_agent": "report_agent",
        "end": END
    }
)

# Return to Master after each agent work
workflow.add_edge("market_agent", "master")
workflow.add_edge("patent_agent", "master")
workflow.add_edge("clinical_agent", "master")
workflow.add_edge("exim_agent", "master")      # Added Return
workflow.add_edge("internal_agent", "master")  # Added Return
workflow.add_edge("web_agent", "master")
workflow.add_edge("report_agent", "master")

app_graph = workflow.compile()
