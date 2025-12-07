from fpdf import FPDF
from langchain_core.messages import AIMessage
import os

def report_agent_node(state):
    """Worker Agent: Generates PDF Report."""
    print("--- REPORT AGENT: Generating PDF ---")
    
    molecule = state.get("query", "Unknown")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"CONFIDENTIAL: Innovation Report for {molecule}", ln=1, align='C')
    pdf.ln(10)
    
    # Market Data
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. IQVIA Market Insights", ln=1)
    pdf.set_font("Arial", size=10)
    m_data = state.get("market_data", {})
    pdf.multi_cell(0, 10, txt=f"Market Size: {m_data.get('market_size_usd')}\nCAGR: {m_data.get('cagr')}")
    pdf.ln(5)

    # Patent Data
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. Patent Landscape (Lens.org)", ln=1)
    pdf.set_font("Arial", size=10)
    for p in state.get("patent_data", [])[:3]:
        pdf.multi_cell(0, 10, txt=f"- {p.get('title')} ({p.get('status')})")
    pdf.ln(5)

    # Save
    filename = f"report_{molecule}.pdf"
    pdf.output(filename)
    
    return {
        "final_report_path": filename,
        "messages": [AIMessage(content=f"Report generated: {filename}")]
    }
