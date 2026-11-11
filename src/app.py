import streamlit as st
import pandas as pd
from google import genai
from src.config import TRIAGED_CSV_PATH, TICKETS_CSV_PATH, GEMINI_API_KEY, GEMINI_MODEL, SHIFT_REPORT_MD_PATH

st.set_page_config(
    page_title="iFood Ops - AI Triage & SLA Monitor",
    page_icon="🛵",
    layout="wide"
)

# Header
st.title("🛵 iFood Operations — AI Triage & SLA Dispatch Monitor")
st.caption("Autonomous Operations Governance • n8n Workflow + Gemini 3 Flash + Streamlit")

# Carregar dados
csv_source = TRIAGED_CSV_PATH if TRIAGED_CSV_PATH.exists() else TICKETS_CSV_PATH

if not csv_source.exists():
    st.error(f"Arquivo de chamados não encontrado em `{csv_source}`. Baixe o CSV da planilha para a pasta `data/`.")
    st.stop()

df = pd.read_csv(csv_source)

# Métricas principais
c1, c2, c3, c4 = st.columns(4)
total_tickets = len(df)
critical_tickets = len(df[df["urgency_sla"].astype(str).str.contains("CRITICAL", na=False)])
triaged_count = len(df[df["status"] == "TRIAGED_BY_AI"])
negative_count = len(df[df["sentiment"] == "Negative"])

c1.metric("Total de Chamados", total_tickets)
c2.metric("SLA Crítico (15m)", critical_tickets, delta="Requer Despacho" if critical_tickets > 0 else "Normal", delta_color="inverse")
c3.metric("Triados por IA", f"{triaged_count}/{total_tickets}")
c4.metric("Sentimento Negativo", negative_count)

st.divider()

# Filtros laterais
st.sidebar.header("Filtros Operacionais")
stakeholders = ["Todos"] + sorted(list(df["stakeholder_type"].dropna().unique()))
selected_stakeholder = st.sidebar.selectbox("Stakeholder", stakeholders)

slas = ["Todos"] + sorted(list(df["urgency_sla"].dropna().unique()))
selected_sla = st.sidebar.selectbox("Urgência / SLA", slas)

filtered_df = df.copy()
if selected_stakeholder != "Todos":
    filtered_df = filtered_df[filtered_df["stakeholder_type"] == selected_stakeholder]
if selected_sla != "Todos":
    filtered_df = filtered_df[filtered_df["urgency_sla"] == selected_sla]

# Visualização da fila operacional
st.subheader("📋 Fila Operacional Triada")
st.dataframe(
    filtered_df[[
        "ticket_id", "order_id", "stakeholder_type", "intent_category",
        "urgency_sla", "sentiment", "recommended_action", "suggested_reply"
    ]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Seção de Resumo Executivo (IA Shift Briefing)
st.subheader("🤖 AI Shift Operations Briefing")
st.write("Gere uma síntese executiva dos incidentes do turno com correlação automática de pedidos via Gemini.")

if st.button("Gerar Shift Briefing com IA", type="primary"):
    if not GEMINI_API_KEY:
        st.warning("Chave `GEMINI_API_KEY` não encontrada no arquivo `.env`.")
    else:
        with st.spinner("Analisando incidentes operacionais e correlações de pedidos..."):
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            prompt = f"""
Você é o Gerente Executivo de Operações do iFood.
Analise os seguintes chamados operacionais que acabaram de ser triados:

{df.to_json(orient='records', force_ascii=False)}

Gere um relatório executivo de passagem de turno estruturado estritamente nas seguintes seções:
1. **Destaques do Turno (Executive Summary)**: Visão geral da saúde da operação.
2. **Incidentes Críticos & Correlações**: Destaque se houve chamados correlacionados (ex: atraso de cliente e pane de moto no mesmo pedido) e o que foi feito.
3. **Ofensores de Merchant e App**: Problemas de repasse ou falhas técnicas em ferramentas de parceiros.
4. **Plano de Ação Imediato**: Próximas 3 medidas para o time de suporte operacional.
"""
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            
            briefing_text = response.text
            SHIFT_REPORT_MD_PATH.write_text(briefing_text, encoding="utf-8")
            st.markdown(briefing_text)
            st.success(f"Relatório gerado e salvo em `{SHIFT_REPORT_MD_PATH}`.")

elif SHIFT_REPORT_MD_PATH.exists():
    st.info("Exibindo o último briefing gerado:")
    st.markdown(SHIFT_REPORT_MD_PATH.read_text(encoding="utf-8"))