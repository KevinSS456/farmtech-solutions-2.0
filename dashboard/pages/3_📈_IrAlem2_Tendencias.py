import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

# ─── CAMINHOS ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent
CAMINHO_CSV = BASE_DIR / "ML" / "outputs" / "previsoes_farmtech.csv"

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FarmTech Solutions - Tendências",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILOS (mesmo design system) ────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
    }
    .main { background-color: #0a0d14; }

    .hero {
        text-align: center;
        padding: 40px 0 28px 0;
        border-bottom: 1px solid #1e2535;
        margin-bottom: 32px;
    }
    .hero-tag {
        display: inline-block;
        background: #0f2027;
        border: 1px solid #1e3a4a;
        color: #4ade80;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 100px;
        margin-bottom: 14px;
    }
    .hero h1 {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
        font-size: 3rem;
        font-weight: 800;
        color: #f1f5f9;
        margin: 0;
        letter-spacing: -0.01em;
        line-height: 1.1;
    }
    .hero h1 span { color: #4ade80; }
    .hero p { color: #64748b; font-size: 0.95rem; margin: 10px 0 0 0; }

    .section-title {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: #1e2535;
    }

    .card {
        background: #111827;
        border: 1px solid #1e2535;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }
    .card-val  { font-family:'Cambria Math', Cambria, Georgia, serif; font-size:1.8rem; font-weight:800; color:#4ade80; }
    .card-lbl  { font-size:0.8rem; color:#64748b; margin-top:4px; letter-spacing:0.04em; }

    .trend-up   { color: #4ade80; }
    .trend-down { color: #f87171; }
</style>
""", unsafe_allow_html=True)

LAYOUT = dict(paper_bgcolor="#0a0d14", plot_bgcolor="#0a0d14",
              font=dict(color="#94a3b8", family="Cambria Math"))

# ─── CARREGAR DADOS ───────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados(mtime):
    df = pd.read_csv(CAMINHO_CSV, parse_dates=["timestamp"])
    return df

try:
    mtime = os.path.getmtime(CAMINHO_CSV)
    df = carregar_dados(mtime)
except FileNotFoundError:
    st.error(f"Arquivo não encontrado em: {CAMINHO_CSV}")
    st.stop()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">📈 Ir Além 2 · Análise de Produtividade</div>
    <h1>Farm<span>Tech</span> Solutions</h1>
    <p>Tendências de Produtividade · FIAP Inteligência Artificial · Fase 4</p>
</div>
""", unsafe_allow_html=True)

# ─── INDICADOR DE TENDÊNCIA ────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Indicador de Tendência — Rendimento</div>', unsafe_allow_html=True)

dia_max = df["dia"].max()
ultimos7 = df[df["dia"] > dia_max - 7]["rendimento"].mean()
anteriores = df[df["dia"] <= dia_max - 7]["rendimento"].mean()
delta = ultimos7 - anteriores
seta = "📈" if delta >= 0 else "📉"
cor_classe = "trend-up" if delta >= 0 else "trend-down"

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-val">{anteriores:.1f}</div>
        <div class="card-lbl">RENDIMENTO MÉDIO (ANTERIOR)</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-val">{ultimos7:.1f}</div>
        <div class="card-lbl">RENDIMENTO MÉDIO (ÚLTIMOS 7 DIAS)</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="card">
        <div class="card-val {cor_classe}">{seta} {delta:+.1f}</div>
        <div class="card-lbl">VARIAÇÃO</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ─── TENDÊNCIA TEMPORAL DO RENDIMENTO ──────────────────────────────────────────
st.markdown('<div class="section-title">📈 Evolução do Rendimento — Janeiro/2025</div>', unsafe_allow_html=True)

fig_tend = go.Figure()
fig_tend.add_trace(go.Scatter(
    x=df["timestamp"], y=df["rendimento"],
    mode="lines", name="Real", line=dict(color="#38bdf8", width=2),
    fill="tozeroy", fillcolor="rgba(56,189,248,0.07)"
))
fig_tend.add_trace(go.Scatter(
    x=df["timestamp"], y=df["rendimento_pred"],
    mode="lines", name="Previsto", line=dict(color="#4ade80", width=2, dash="dash")
))
fig_tend.update_layout(
    title="Rendimento Real vs Previsto ao longo do mês",
    title_x=0.5, height=420,
    legend=dict(bgcolor="#111827", bordercolor="#1e2535"),
    **LAYOUT
)
fig_tend.update_xaxes(gridcolor="#1e2535")
fig_tend.update_yaxes(gridcolor="#1e2535")
st.plotly_chart(fig_tend, width="stretch")

st.markdown("---")

# ─── MÉDIAS POR SEMANA ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📆 Rendimento Médio por Semana</div>', unsafe_allow_html=True)

df["semana"] = df["dia"].apply(
    lambda d: "S1" if d <= 7 else "S2" if d <= 14 else "S3" if d <= 21 else "S4"
)
medias_semana = df.groupby("semana")["rendimento"].mean().reindex(["S1", "S2", "S3", "S4"]).reset_index()

cores_semana = {"S1": "#4ade80", "S2": "#38bdf8", "S3": "#fb923c", "S4": "#a78bfa"}

fig_semana = px.bar(
    medias_semana, x="semana", y="rendimento",
    color="semana", color_discrete_map=cores_semana,
    title="Rendimento Médio por Semana",
    text_auto=".1f"
)
fig_semana.update_layout(showlegend=False, title_x=0.5, height=380, **LAYOUT)
fig_semana.update_xaxes(gridcolor="#1e2535", title="Semana")
fig_semana.update_yaxes(gridcolor="#1e2535", title="Rendimento Médio")
st.plotly_chart(fig_semana, width="stretch")

st.markdown("---")

# ─── CORRELAÇÃO NPK x RENDIMENTO ────────────────────────────────────────────────
st.markdown('<div class="section-title">🌿 Relação entre NPK e Rendimento</div>', unsafe_allow_html=True)

nutriente = st.selectbox("Selecione o nutriente", ["nitrogenio", "fosforo", "potassio"],
                          format_func=lambda x: {"nitrogenio": "Nitrogênio (N)",
                                                  "fosforo": "Fósforo (P)",
                                                  "potassio": "Potássio (K)"}[x])

fig_npk = px.scatter(
    df, x=nutriente, y="rendimento",
    color_discrete_sequence=["#4ade80"],
    trendline="ols",
    title=f"{nutriente.capitalize()} vs Rendimento"
)
fig_npk.update_layout(title_x=0.5, height=400, **LAYOUT)
fig_npk.update_xaxes(gridcolor="#1e2535")
fig_npk.update_yaxes(gridcolor="#1e2535")
st.plotly_chart(fig_npk, width="stretch")

# ─── RODAPÉ ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#334155; font-size:0.78rem;'>"
    "FarmTech Solutions © 2025 — FIAP Inteligência Artificial — Ir Além 2"
    "</p>",
    unsafe_allow_html=True
)