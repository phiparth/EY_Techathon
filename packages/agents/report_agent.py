from fpdf import FPDF
from langchain_core.messages import AIMessage
import os

# Custom PDF class to handle UTF-8 symbols slightly better if needed, 
# but standard FPDF is fine for this hackathon.
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Techathon 6.0: Agentic AI Innovation Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def report_agent_node(state):
    """Worker Agent: Generates a comprehensive PDF Report including ALL agents."""
    print("--- REPORT AGENT: Generating PDF ---")
    
    molecule = state.get("query", "Unknown Molecule")
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=f"Molecule Analysis: {molecule}", ln=1, align='L')
    pdf.ln(5)

    # ---------------------------------------------------------
    # 1. MARKET DATA (IQVIA)
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(200, 220, 255) # Light blue header
    pdf.cell(0, 10, txt="1. IQVIA Market Insights", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    m_data = state.get("market_data")
    if m_data:
        text = (
            f"Market Size: {m_data.get('market_size_usd', 'N/A')}\n"
            f"CAGR: {m_data.get('cagr', 'N/A')}\n"
            f"Top Competitors: {', '.join(m_data.get('top_competitors', []))}\n"
            f"Growth Region: {m_data.get('growth_region', 'N/A')}"
        )
        pdf.multi_cell(0, 8, txt=text)
    else:
        pdf.multi_cell(0, 8, txt="No market data available.")
    pdf.ln(5)

    # ---------------------------------------------------------
    # 2. PATENT LANDSCAPE (Lens.org)
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="2. Patent Landscape (Lens.org)", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    p_data = state.get("patent_data")
    if p_data:
        for i, p in enumerate(p_data[:5]): # Limit to top 5
            title = p.get('title', 'Unknown Title').encode('latin-1', 'replace').decode('latin-1')
            status = p.get('status', 'Unknown')
            pdf.multi_cell(0, 6, txt=f"{i+1}. {title} ({status})")
    else:
        pdf.multi_cell(0, 8, txt="No patent data found.")
    pdf.ln(5)

    # ---------------------------------------------------------
    # 3. CLINICAL TRIALS (ClinicalTrials.gov)
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="3. Clinical Trials Status", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    c_data = state.get("clinical_data")
    if c_data:
        for i, trial in enumerate(c_data[:5]):
            title = trial.get('title', 'No Title').encode('latin-1', 'replace').decode('latin-1')
            status = trial.get('status', 'Unknown')
            nct_id = trial.get('nct_id', 'N/A')
            pdf.multi_cell(0, 6, txt=f"- [{nct_id}] {title}\n  Status: {status}")
            pdf.ln(2)
    else:
        pdf.multi_cell(0, 8, txt="No clinical trials found.")
    pdf.ln(5)

    # ---------------------------------------------------------
    # 4. EXIM TRENDS
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="4. Export/Import Trends", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    e_data = state.get("exim_data")
    if e_data:
        text = (
            f"Major Importers: {', '.join(e_data.get('major_importers', []))}\n"
            f"Supply Risk: {e_data.get('supply_risk', 'N/A')}\n"
            f"Primary Sources: {e_data.get('api_source', 'N/A')}"
        )
        pdf.multi_cell(0, 8, txt=text)
    else:
        pdf.multi_cell(0, 8, txt="No trade data available.")
    pdf.ln(5)

    # ---------------------------------------------------------
    # 5. WEB INTELLIGENCE
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="5. Web Search Intelligence", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    w_data = state.get("web_data")
    if w_data:
        # Sanitize text for PDF (remove emojis/complex chars)
        clean_web = w_data.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, txt=clean_web)
    else:
        pdf.multi_cell(0, 8, txt="Web search returned no results.")
    pdf.ln(5)

    # ---------------------------------------------------------
    # 6. INTERNAL STRATEGY
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="6. Internal Strategy Alignment", ln=1, fill=True)
    pdf.set_font("Arial", size=10)
    
    i_data = state.get("internal_data")
    if i_data:
        clean_internal = i_data.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, txt=clean_internal)
    else:
        pdf.multi_cell(0, 8, txt="No internal documents matched.")

    # Save
    filename = f"report_{molecule}.pdf"
    pdf.output(filename)
    
    return {
        "final_report_path": filename,
        "messages": [AIMessage(content=f"Report generated: {filename}")]
    }
