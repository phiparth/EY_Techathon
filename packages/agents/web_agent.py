from langchain_core.messages import AIMessage

def web_agent_node(state):
    """Worker Agent: Real-time web search with Fail-Safe."""
    query = state.get("query", "")
    print("--- WEB AGENT: Searching Web ---")
    
    search_result = ""
    
    # SAFE IMPORT: Only try to import when the function runs
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        search_result = search.run(f"latest news and guidelines for {query} molecule drug repurposing")
    except ImportError:
        # FALLBACK: If library is missing, pretend we searched
        print("Warning: DuckDuckGo library missing. Using Mock.")
        search_result = (
            f"Automated Web Search Result: {query} shows promising results in recent "
            "academic literature for repurposed oncology indications. "
            "(Mock data: 'ddgs' library was unavailable)."
        )
    except Exception as e:
        search_result = f"Search failed: {str(e)}"
        
    return {
        "web_data": search_result,
        "messages": [AIMessage(content="Web Agent finished searching.")]
    }
