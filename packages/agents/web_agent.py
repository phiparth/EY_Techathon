from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import AIMessage

def web_agent_node(state):
    """Worker Agent: Real-time web search for news/guidelines."""
    query = state.get("query", "")
    print("--- WEB AGENT: Searching Web ---")
    
    search = DuckDuckGoSearchRun()
    try:
        res = search.run(f"latest news and guidelines for {query} molecule drug repurposing")
    except:
        res = "Web search failed or rate limited."
        
    return {
        "web_data": res,
        "messages": [AIMessage(content="Web Agent finished searching.")]
    }
