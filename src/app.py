import sys
from pathlib import Path

# Add project root directory to sys.path to resolve module imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from google import genai
from src.config import (
    TRIAGED_CSV_PATH,
    TICKETS_CSV_PATH,
    GOOGLE_SHEET_CSV_URL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    SHIFT_REPORT_MD_PATH,
)

st.set_page_config(
    page_title="iFood Ops - AI Triage & SLA Monitor",
    page_icon="🛵",
    layout="wide"
)


@st.cache_data(ttl=15)
def load_live_operations_data() -> tuple[pd.DataFrame, str]:
    """Fetch live triaged data directly from Google Sheets with local CSV fallback."""
    try:
        df_live = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        if "ticket_id" in df_live.columns and len(df_live) > 0:
            # Automatically cache a local copy for offline reproducibility
            TRIAGED_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
            df_live.to_csv(TRIAGED_CSV_PATH, index=False)
            return df_live, "Live Google Sheets Sync"
    except Exception:
        pass

    if TRIAGED_CSV_PATH.exists():
        return pd.read_csv(TRIAGED_CSV_PATH), "Local Triaged CSV Cache"
    if TICKETS_CSV_PATH.exists():
        return pd.read_csv(TICKETS_CSV_PATH), "Seed CSV (Untriaged Fallback)"
    return pd.DataFrame(), "No Data Source Available"


# Application Header
col_title, col_sync = st.columns([4, 1])
with col_title:
    st.title("🛵 iFood Operations — AI Triage & SLA Dispatch Monitor")
    st.caption("Autonomous Operations Governance • n8n Workflow + Gemini 3 Flash + Live Google Sheets")
with col_sync:
    st.write("")
    if st.button("🔄 Sync Live Sheets", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

df, data_source_label = load_live_operations_data()

if df.empty:
    st.error("No operational tickets found. Verify your Google Sheets sharing permissions or local CSV.")
    st.stop()

st.sidebar.caption(f"📡 **Data Source:** {data_source_label}")

# Core Operational KPIs
c1, c2, c3, c4 = st.columns(4)
total_tickets = len(df)
critical_tickets = len(df[df["urgency_sla"].astype(str).str.contains("CRITICAL", na=False)])
triaged_count = len(df[df["status"] == "TRIAGED_BY_AI"])
negative_count = len(df[df["sentiment"] == "Negative"])

c1.metric("Total Ingested Tickets", total_tickets)
c2.metric(
    "Critical SLA (15m)",
    critical_tickets,
    delta="Immediate Dispatch Required" if critical_tickets > 0 else "Nominal",
    delta_color="inverse"
)
c3.metric("AI Triage Automation Rate", f"{(triaged_count / total_tickets * 100):.0f}%" if total_tickets else "0%")
c4.metric("Negative Sentiment Rate", f"{(negative_count / total_tickets * 100):.0f}%" if total_tickets else "0%")

st.divider()

# Sidebar Filters
st.sidebar.header("Operational Filters")
stakeholders = ["All"] + sorted([
    str(s) for s in df["stakeholder_type"].dropna().unique()
    if str(s).strip() and str(s).lower() != "nan"
])
selected_stakeholder = st.sidebar.selectbox("Stakeholder", stakeholders)

slas = ["All"] + sorted([
    str(s) for s in df["urgency_sla"].dropna().unique()
    if str(s).strip() and str(s).lower() != "nan"
])
selected_sla = st.sidebar.selectbox("Urgency / SLA Tier", slas)

filtered_df = df.copy()
if selected_stakeholder != "All":
    filtered_df = filtered_df[filtered_df["stakeholder_type"] == selected_stakeholder]
if selected_sla != "All":
    filtered_df = filtered_df[filtered_df["urgency_sla"] == selected_sla]

# Live Operational Queue
st.subheader("📋 Live Triaged Incident Queue")
display_cols = [
    col for col in [
        "ticket_id", "order_id", "stakeholder_type", "intent_category",
        "urgency_sla", "sentiment", "recommended_action", "suggested_reply"
    ] if col in filtered_df.columns
]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

st.divider()

# AI Shift Operations Briefing
st.subheader("🤖 AI Shift Operations Briefing")
st.write("Synthesize operational incidents, cross-correlate related order IDs, and produce executive action items.")

if st.button("Generate Executive Shift Briefing", type="primary"):
    if not GEMINI_API_KEY:
        st.warning("Missing `GEMINI_API_KEY` in environment variables or `.env` file.")
    else:
        with st.spinner("Analyzing cross-stakeholder order events and dispatch logs..."):
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            prompt = f"""
You are the Head of Operations at iFood.
Review the following operational incident batch processed by the autonomous triage pipeline:

{df.to_json(orient='records', force_ascii=False)}

Generate a crisp executive shift handover report structured strictly under these sections:
1. **Shift Overview & Health**: Summary of triage velocity, SLA distribution, and network sentiment.
2. **Critical Incidents & Order Correlation**: Specifically analyze whether multiple tickets correlate to the same order (e.g., customer delay complaints tied to courier mechanical breakdowns on the same order_id) and document mitigation.
3. **Merchant & Technical Outliers**: Outline finance payout claims, POS bugs, or vendor pain points.
4. **Immediate 30-Minute Action Items**: Three concrete directives for duty dispatchers.
"""
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            
            briefing_text = response.text
            SHIFT_REPORT_MD_PATH.write_text(briefing_text, encoding="utf-8")
            st.markdown(briefing_text)
            st.success(f"Shift report successfully compiled and saved to `{SHIFT_REPORT_MD_PATH}`.")

elif SHIFT_REPORT_MD_PATH.exists():
    st.info("Displaying latest compiled shift briefing:")
    st.markdown(SHIFT_REPORT_MD_PATH.read_text(encoding="utf-8"))