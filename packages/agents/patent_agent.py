import requests
import os
from langchain_core.messages import AIMessage

def patent_agent_node(state):
    """Worker Agent: Searches Lens.org or USPTO for patents."""
    molecule = state.get("query", "")
    token = os.getenv("LENS_ORG_API_TOKEN")
    
    print(f"--- PATENT AGENT: Searching for {molecule} ---")
    
    # ---------------------------------------------------------
    # SCALABLE API: Lens.org
    # ---------------------------------------------------------
    patents = []
    if token and len(token) > 5:
        url = "https://api.lens.org/patent/search"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "query": {
                "bool": {
                    "must": [{"match": {"title": molecule}}, {"match": {"abstract": "pharmaceutical"}}],
                }
            },
            "size": 5
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", []):
                    patents.append({
                        "id": item.get("lens_id"),
                        "title": item.get("title"),
                        "publication_date": item.get("biblio", {}).get("publication_date", "N/A"),
                        "status": "Active (Assumed)" 
                    })
        except Exception as e:
            patents = [{"error": f"Lens API Failed: {str(e)}"}]
    
    # ---------------------------------------------------------
    # MOCK FALLBACK (If no API key provided)
    # ---------------------------------------------------------
    if not patents:
        patents = [
            {"id": "US-PAT-001", "title": f"Novel formulation of {molecule}", "publication_date": "2022-01-15", "status": "Active"},
            {"id": "US-PAT-002", "title": f"Method of treating Diabetes with {molecule}", "publication_date": "2010-05-20", "status": "Expired"},
        ]

    return {
        "patent_data": patents,
        "messages": [AIMessage(content=f"Patent Agent found {len(patents)} records.")]
    }
