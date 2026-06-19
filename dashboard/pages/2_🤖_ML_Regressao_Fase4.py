import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import os


# ─── CAMINHOS ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent  # sobe de pages/ -> dashboard/ -> raiz
CAMINHO_CSV = BASE_DIR / "ML" / "outputs" / "previsoes_farmtech.csv"


@st.cache_data
def carregar_dados(mtime):
    df = pd.read_csv(CAMINHO_CSV, parse_dates=["timestamp"])
    return df

mtime = os.path.getmtime(CAMINHO_CSV)
df = carregar_dados(mtime)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FarmTech Solutions - ML",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILOS (mesmo design system da Fase 3) ──────────────────────────────────
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

    .metric-card {
        background: #111827;
        border: 1px solid #1e2535;
        border-radius: 14px;
        padding: 18px;
    }
</style>
""", unsafe_allow_html=True)

LAYOUT = dict(paper_bgcolor="#0a0d14", plot_bgcolor="#0a0d14",
              font=dict(color="#94a3b8", family="Cambria Math"))

# ─── CARREGAR DADOS ───────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV, parse_dates=["timestamp"])
    return df

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error(f"Arquivo não encontrado em: {CAMINHO_CSV}")
    st.stop()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🤖 Machine Learning · Regressão Supervisionada</div>
    <h1>Farm<span>Tech</span> Solutions</h1>
    <p>Previsão de Variáveis Agrícolas · FIAP Inteligência Artificial · Fase 4</p>
</div>
""", unsafe_allow_html=True)

# ─── MÉTRICAS POR TARGET ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">📐 Métricas de Desempenho dos Modelos</div>', unsafe_allow_html=True)

targets = {
    "umidade":    "💧 Umidade do Solo",
    "ph":         "🧪 pH do Solo",
    "rendimento": "🌾 Rendimento Estimado"
}

cols = st.columns(3)
metricas_calc = {}

for col, (target, label) in zip(cols, targets.items()):
    mae  = mean_absolute_error(df[target], df[f"{target}_pred"])
    rmse = np.sqrt(mean_squared_error(df[target], df[f"{target}_pred"]))
    r2   = r2_score(df[target], df[f"{target}_pred"])
    metricas_calc[target] = {"mae": mae, "rmse": rmse, "r2": r2}

    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-lbl" style="margin-bottom:10px;">{label}</div>
            <div style="display:flex; justify-content:space-between;">
                <div style="text-align:center;">
                    <div class="card-val" style="font-size:1.3rem;">{mae:.2f}</div>
                    <div class="card-lbl">MAE</div>
                </div>
                <div style="text-align:center;">
                    <div class="card-val" style="font-size:1.3rem;">{rmse:.2f}</div>
                    <div class="card-lbl">RMSE</div>
                </div>
                <div style="text-align:center;">
                    <div class="card-val" style="font-size:1.3rem;">{r2:.2f}</div>
                    <div class="card-lbl">R²</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ─── MAPA DE CORRELAÇÃO ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Mapa de Correlação entre Variáveis</div>', unsafe_allow_html=True)

corr_cols = ["umidade", "ph", "rendimento", "nitrogenio", "fosforo", "potassio", "chuva"]
corr = df[corr_cols].corr()

fig_corr = px.imshow(
    corr, text_auto=".2f", color_continuous_scale="RdBu_r",
    aspect="auto", zmin=-1, zmax=1
)
fig_corr.update_layout(height=420, title_x=0.5, **LAYOUT)
st.plotly_chart(fig_corr, width="stretch")

st.markdown("---")

# ─── PREVISTO VS REAL ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🔍 Previsto vs Real</div>', unsafe_allow_html=True)

target_escolhido = st.selectbox("Selecione a variável", list(targets.keys()),
                                  format_func=lambda t: targets[t])

col_a, col_b = st.columns(2)

with col_a:
    fig_linha = go.Figure()
    fig_linha.add_trace(go.Scatter(
        x=df["timestamp"], y=df[target_escolhido],
        mode="lines", name="Real", line=dict(color="#38bdf8", width=2)
    ))
    fig_linha.add_trace(go.Scatter(
        x=df["timestamp"], y=df[f"{target_escolhido}_pred"],
        mode="lines", name="Previsto", line=dict(color="#4ade80", width=2, dash="dash")
    ))
    fig_linha.update_layout(
        title=f"{targets[target_escolhido]} — Série Temporal",
        title_x=0.5, height=380,
        legend=dict(bgcolor="#111827", bordercolor="#1e2535"),
        **LAYOUT
    )
    fig_linha.update_xaxes(gridcolor="#1e2535")
    fig_linha.update_yaxes(gridcolor="#1e2535")
    st.plotly_chart(fig_linha, width="stretch")

with col_b:
    fig_scatter = px.scatter(
        df, x=target_escolhido, y=f"{target_escolhido}_pred",
        trendline="ols",
        color_discrete_sequence=["#4ade80"],
        title=f"Dispersão — {targets[target_escolhido]}"
    )
    fig_scatter.update_layout(title_x=0.5, height=380, **LAYOUT)
    fig_scatter.update_xaxes(title="Real", gridcolor="#1e2535")
    fig_scatter.update_yaxes(title="Previsto", gridcolor="#1e2535")
    st.plotly_chart(fig_scatter, width="stretch")

st.markdown("---")

st.markdown("---")

# ─── SISTEMA DE RECOMENDAÇÕES AUTOMÁTICAS ──────────────────────────────────────
st.markdown('<div class="section-title">🌿 Sistema de Recomendações Automáticas</div>', unsafe_allow_html=True)

ultimo_pred = df.iloc[-1]

recomendacoes = []

# Umidade
if ultimo_pred["umidade_pred"] < 60:
    recomendacoes.append(("💧", "IRRIGAR", f"Umidade prevista em {ultimo_pred['umidade_pred']:.1f}% — abaixo do ideal (60–80%)", "warning"))
elif ultimo_pred["umidade_pred"] > 80:
    recomendacoes.append(("⚠️", "NÃO IRRIGAR", f"Umidade prevista em {ultimo_pred['umidade_pred']:.1f}% — solo tende a encharcar", "error"))
else:
    recomendacoes.append(("✅", "UMIDADE OK", f"Umidade prevista em {ultimo_pred['umidade_pred']:.1f}% — dentro da faixa ideal", "success"))

# Chuva
if ultimo_pred["chuva"] == 1:
    recomendacoes.append(("🌧️", "SUSPENDER IRRIGAÇÃO", "Previsão de chuva detectada", "warning"))

# pH
if ultimo_pred["ph_pred"] < 6.0:
    recomendacoes.append(("🧪", "APLICAR CALCÁRIO DOLOMÍTICO", f"pH previsto em {ultimo_pred['ph_pred']:.2f} — abaixo do ideal (6.0–6.5)", "warning"))
elif ultimo_pred["ph_pred"] > 6.5:
    recomendacoes.append(("🧪", "APLICAR ENXOFRE AGRÍCOLA", f"pH previsto em {ultimo_pred['ph_pred']:.2f} — acima do ideal (6.0–6.5)", "warning"))
else:
    recomendacoes.append(("✅", "pH OK", f"pH previsto em {ultimo_pred['ph_pred']:.2f} — dentro da faixa ideal", "success"))

# NPK
if ultimo_pred["nitrogenio"] < 80:
    recomendacoes.append(("🌿", "APLICAR UREIA / NITRATO DE AMÔNIO", f"Nitrogênio em {ultimo_pred['nitrogenio']:.1f} mg/kg — abaixo do mínimo (80 mg/kg)", "warning"))

if ultimo_pred["fosforo"] < 30:
    recomendacoes.append(("🌿", "APLICAR SUPERFOSFATO SIMPLES", f"Fósforo em {ultimo_pred['fosforo']:.1f} mg/kg — abaixo do mínimo (30 mg/kg)", "warning"))

if ultimo_pred["potassio"] < 100:
    recomendacoes.append(("🌿", "APLICAR CLORETO DE POTÁSSIO", f"Potássio em {ultimo_pred['potassio']:.1f} mg/kg — abaixo do mínimo (100 mg/kg)", "warning"))

# Rendimento esperado
rendimento_status = "✅ Bom" if ultimo_pred["rendimento_pred"] >= 50 else "⚠️ Abaixo do esperado"
recomendacoes.append(("🌾", f"RENDIMENTO ESTIMADO: {ultimo_pred['rendimento_pred']:.1f}", rendimento_status, 
                       "success" if ultimo_pred["rendimento_pred"] >= 50 else "warning"))

# Exibir recomendações
col_esq, col_dir = st.columns(2)
for i, (icone, titulo, descricao, tipo) in enumerate(recomendacoes):
    coluna = col_esq if i % 2 == 0 else col_dir
    with coluna:
        if tipo == "success":
            st.success(f"{icone} **{titulo}** — {descricao}")
        elif tipo == "error":
            st.error(f"{icone} **{titulo}** — {descricao}")
        else:
            st.warning(f"{icone} **{titulo}** — {descricao}")

# ─── FILTRO POR DIA ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📅 Detalhamento por Dia</div>', unsafe_allow_html=True)

dia = st.slider("Dia de janeiro/2025", int(df["dia"].min()), int(df["dia"].max()), int(df["dia"].min()))
df_dia = df[df["dia"] == dia]

colunas_tabela = ["timestamp"] + list(targets.keys()) + [f"{t}_pred" for t in targets.keys()]
st.dataframe(df_dia[colunas_tabela], width="stretch", hide_index=True)

# ─── RODAPÉ ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#334155; font-size:0.78rem;'>"
    "FarmTech Solutions © 2025 — FIAP Inteligência Artificial — Fase 4"
    "</p>",
    unsafe_allow_html=True
)