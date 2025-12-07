import streamlit as st
from packages.orchestrator import app_graph
import time

st.set_page_config(page_title="Pharma Agentic AI", layout="wide")

st.title("Techathon 6.0: Pharmaceutical Master Agent")
st.markdown("### Orchestrating 7 Specialized Agents for Molecule Repurposing")

# Input
query = st.text_input("Enter Molecule Name (e.g., 'Metformin'):", "Metformin")

if st.button("Start Innovation Scan"):
    # Initial State
    initial_state = {
        "query": query,
        "messages": [],
        "market_data": None,
        "patent_data": None,
        "clinical_data": None,
        "web_data": None,
        "final_report_path": None
    }
    
    # Visualization Container
    status_col, chat_col = st.columns([1, 2])
    
    with status_col:
        st.subheader("Agent Activation Status")
        status_box = st.empty()
        
    with chat_col:
        st.subheader("Master Agent Log")
        log_box = st.container()

    # Run Graph
    try:
        for output in app_graph.stream(initial_state):
            for key, value in output.items():
                # Visualize Agent Activity
                if key == "market_agent":
                    status_box.info("✅ IQVIA Insights Agent: Finished analysis")
                    with log_box:
                        st.write(f"**IQVIA:** {value['market_data']}")
                        
                elif key == "patent_agent":
                    status_box.info("✅ Patent Landscape Agent: Finished search")
                    with log_box:
                        st.write(f"**Lens.org:** Found {len(value['patent_data'])} patents")
                        
                elif key == "clinical_agent":
                    status_box.info("✅ Clinical Trials Agent: Finished search")
                    with log_box:
                        st.write(f"**ClinicalTrials.gov:** Found {len(value['clinical_data'])} trials")
                        
                elif key == "report_agent":
                    status_box.success("✅ Report Generator: PDF Created")
                    pdf_path = value['final_report_path']
                    with open(pdf_path, "rb") as f:
                        st.download_button("Download Innovation Report", f, file_name=pdf_path)
                
                time.sleep(0.5) # UI pacing
                
    except Exception as e:
        st.error(f"Error executing agent pipeline: {e}")
