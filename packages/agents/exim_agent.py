from langchain_core.messages import AIMessage

def exim_agent_node(state):
    """Worker Agent: Queries Export/Import Data."""
    print("--- EXIM AGENT: Fetching Trade Data ---")
    
    data = {
        "major_importers": ["USA", "Germany", "India"],
        "supply_risk": "Moderate",
        "api_source": "China (60%), India (30%)"
    }
    
    return {
        "exim_data": data,
        "messages": [AIMessage(content="EXIM Agent retrieved trade flows.")]
    }
