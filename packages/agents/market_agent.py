from langchain_core.messages import AIMessage

def market_agent_node(state):
    """Worker Agent: Queries IQVIA Mock Database."""
    print("--- IQVIA AGENT: Fetching Market Data ---")
    
    # In real world: requests.post("https://api.iqvia.com/...", ...)
    data = {
        "market_size_usd": "14.2 Billion",
        "cagr": "5.8%",
        "top_competitors": ["Pfizer", "Merck", "GenericCo"],
        "growth_region": "North America & APAC"
    }
    
    return {
        "market_data": data,
        "messages": [AIMessage(content="IQVIA Agent retrieved market stats.")]
    }
