from langchain_core.messages import AIMessage

def internal_agent_node(state):
    """Worker Agent: Searches internal PDFs/Docs."""
    print("--- INTERNAL AGENT: Reading Internal Docs ---")
    
    # In production: Use RAG (Chroma/Pinecone) here.
    # For Hackathon: Return mock internal strategy data
    
    internal_insight = """
    INTERNAL MEMO: Strategy Deck Q3
    - We have excess capacity for solid oral dosage forms.
    - Targeting therapeutic areas: Oncology and Metabolic disorders.
    - Avoid crowded markets like standard Metformin generics.
    """
    
    return {
        "internal_data": internal_insight,
        "messages": [AIMessage(content="Internal Agent retrieved strategy docs.")]
    }
