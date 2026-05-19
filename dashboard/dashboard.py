import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FarmTech Solutions",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── ESTILOS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
    }

    [data-testid="stSidebar"]      { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    .main { background-color: #0a0d14; }

    /* HEADER */
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
    .hero p {
        color: #64748b;
        font-size: 0.95rem;
        margin: 10px 0 0 0;
        font-weight: 400;
    }

    /* SECTION TITLE */
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

    /* CARDS GENÉRICOS */
    .card {
        background: #111827;
        border: 1px solid #1e2535;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }
    .card-val  { font-family:'Cambria Math', Cambria, Georgia, serif; font-size:1.8rem; font-weight:800; color:#4ade80; }
    .card-lbl  { font-size:0.8rem; color:#64748b; margin-top:4px; letter-spacing:0.04em; }

    /* SEMANA CARDS */
    .semana-wrap {
        background: #111827;
        border: 1px solid #1e2535;
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        transition: border-color .2s;
    }
    .semana-wrap.ativo { border-color: #4ade80; }
    .semana-badge {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .semana-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        border-bottom: 1px solid #1e2535;
        font-size: 0.78rem;
    }
    .semana-row:last-child { border-bottom: none; }
    .semana-row-lbl { color: #64748b; }
    .semana-row-val { color: #e2e8f0; font-weight: 600; }
    .semana-bomba-val {
        font-family: 'Cambria Math', Cambria, Georgia, serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #4ade80;
        margin: 8px 0 2px 0;
    }
    .semana-bomba-lbl { font-size: 0.72rem; color: #64748b; }

    /* STATUS */
    .status-on {
        background: #0a1f0f;
        border: 1px solid #16a34a;
        border-radius: 10px;
        padding: 14px;
        color: #4ade80;
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
    }
    .status-off {
        background: #1a0a0a;
        border: 1px solid #dc2626;
        border-radius: 10px;
        padding: 14px;
        color: #f87171;
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ─── CARREGAR DADOS ───────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("sensores_farmtech_v2.csv", parse_dates=["timestamp"])
    return df

df = carregar_dados()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">☕ Lavoura de Café — Monitoramento em Tempo Real</div>
    <h1>Farm<span>Tech</span> Solutions</h1>
    <p>Sistema Inteligente de Irrigação · FIAP Inteligência Artificial · Fase 3</p>
</div>
""", unsafe_allow_html=True)

# ─── FILTRO DE PERÍODO ────────────────────────────────────────────────────────
data_min = df["timestamp"].min().date()
data_max = df["timestamp"].max().date()

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    data_inicio, data_fim = st.date_input(
        "📅 Período",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )

df_filtrado = df[
    (df["timestamp"].dt.date >= data_inicio) &
    (df["timestamp"].dt.date <= data_fim)
].copy()

df_filtrado["semana"] = df_filtrado["timestamp"].apply(
    lambda dt: "S1" if dt.day <= 7 else "S2" if dt.day <= 14 else "S3" if dt.day <= 21 else "S4"
)
df_filtrado["data"] = df_filtrado["timestamp"].dt.date

ultimo = df_filtrado.iloc[-1]

st.markdown("<br>", unsafe_allow_html=True)

# ─── LEITURA ATUAL ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📡 Leitura Mais Recente</div>', unsafe_allow_html=True)

cols = st.columns(6)
cards_data = [
    (f"{ultimo['umidade']}%",   "💧 Umidade"),
    (f"{ultimo['ph']}",         "🧪 pH"),
    (f"{ultimo['nitrogenio']}", "🌿 N mg/kg"),
    (f"{ultimo['fosforo']}",    "🔬 P mg/kg"),
    (f"{ultimo['potassio']}",   "⚡ K mg/kg"),
    ("🌧️ Sim" if ultimo['chuva'] == 1 else "☀️ Não", "🌦️ Chuva"),
]
for col, (val, lbl) in zip(cols, cards_data):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-val">{val}</div>
            <div class="card-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_bomb, col_sugest = st.columns([1, 2])
with col_bomb:
    st.markdown('<div class="section-title">🚿 Status</div>', unsafe_allow_html=True)
    if ultimo['irrigacao'] == 1:
        st.markdown('<div class="status-on">✅ BOMBA LIGADA</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-off">❌ BOMBA DESLIGADA</div>', unsafe_allow_html=True)

with col_sugest:
    st.markdown('<div class="section-title">💡 Sugestão</div>', unsafe_allow_html=True)
    problemas = []
    if ultimo['umidade'] >= 60:
        problemas.append(f"• Umidade alta ({ultimo['umidade']}%) — solo não precisa de água")
    if not (5.5 <= ultimo['ph'] <= 7.0):
        problemas.append(f"• pH fora da faixa ({ultimo['ph']}) — corrigir solo")
    if ultimo['nitrogenio'] < 80:
        problemas.append(f"• Nitrogênio baixo ({ultimo['nitrogenio']} mg/kg) — aplicar fertilizante N")
    if ultimo['fosforo'] < 30:
        problemas.append(f"• Fósforo baixo ({ultimo['fosforo']} mg/kg) — aplicar fertilizante P")
    if ultimo['potassio'] < 100:
        problemas.append(f"• Potássio baixo ({ultimo['potassio']} mg/kg) — aplicar fertilizante K")
    if ultimo['chuva'] == 1:
        problemas.append("• Chuva prevista — irrigação suspensa automaticamente")
    if not problemas:
        st.success("✅ Todas as condições ideais! Irrigação recomendada.")
    else:
        for p in problemas:
            st.warning(p)

st.markdown("---")

# ─── VISÃO SEMANAL ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📆 Visão Semanal — Médias + Ativações da Bomba</div>', unsafe_allow_html=True)

semanas_ordem  = ["S1", "S2", "S3", "S4"]
semanas_ranges = {"S1": "dias 1–7", "S2": "dias 8–14", "S3": "dias 15–21", "S4": "dias 22–31"}
cores_semana   = {"S1": "#4ade80", "S2": "#38bdf8", "S3": "#fb923c", "S4": "#a78bfa"}

# Calcular médias e ativações por semana
resumo_semanas = df_filtrado.groupby("semana").agg(
    umidade   =("umidade",    "mean"),
    ph        =("ph",         "mean"),
    nitrogenio=("nitrogenio", "mean"),
    fosforo   =("fosforo",    "mean"),
    potassio  =("potassio",   "mean"),
    bomba     =("irrigacao",  "sum"),
    chuva     =("chuva",      "sum"),
).reindex(semanas_ordem)

# Filtro de semana
cf, _ = st.columns([3, 1])
with cf:
    semana_sel = st.radio(
        "Filtrar:",
        ["Todas"] + semanas_ordem,
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Cards semanais
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
for col, s in zip([col_s1, col_s2, col_s3, col_s4], semanas_ordem):
    with col:
        r = resumo_semanas.loc[s]
        ativo = semana_sel == s or semana_sel == "Todas"
        borda_class = "ativo" if ativo else ""
        cor = cores_semana[s]
        bomba_val = int(r['bomba']) if not pd.isna(r['bomba']) else 0

        def fmt(v): return f"{v:.1f}" if not pd.isna(v) else "—"

        st.markdown(f"""
        <div class="semana-wrap {borda_class}" style="border-color:{''+cor if ativo else '#1e2535'};">
            <div class="semana-badge" style="color:{cor};">{s} · {semanas_ranges[s]}</div>
            <div class="semana-bomba-val">{bomba_val}</div>
            <div class="semana-bomba-lbl">🚿 ativações da bomba</div>
            <br>
            <div class="semana-row">
                <span class="semana-row-lbl">💧 Umidade</span>
                <span class="semana-row-val">{fmt(r['umidade'])}%</span>
            </div>
            <div class="semana-row">
                <span class="semana-row-lbl">🧪 pH</span>
                <span class="semana-row-val">{fmt(r['ph'])}</span>
            </div>
            <div class="semana-row">
                <span class="semana-row-lbl">🌿 N</span>
                <span class="semana-row-val">{fmt(r['nitrogenio'])} mg/kg</span>
            </div>
            <div class="semana-row">
                <span class="semana-row-lbl">🔬 P</span>
                <span class="semana-row-val">{fmt(r['fosforo'])} mg/kg</span>
            </div>
            <div class="semana-row">
                <span class="semana-row-lbl">⚡ K</span>
                <span class="semana-row-val">{fmt(r['potassio'])} mg/kg</span>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Gráfico de barras das ativações por semana
if semana_sel == "Todas":
    df_graf = df_filtrado
else:
    df_graf = df_filtrado[df_filtrado["semana"] == semana_sel]

irrig_dia = df_graf.groupby(["data", "semana"])["irrigacao"].sum().reset_index()
irrig_dia.columns = ["data", "semana", "ativacoes"]

fig_sem = px.bar(
    irrig_dia, x="data", y="ativacoes", color="semana",
    title="Ativações da Bomba por Dia",
    color_discrete_map=cores_semana,
    category_orders={"semana": semanas_ordem}
)
fig_sem.update_layout(
    height=300,
    paper_bgcolor="#0a0d14", plot_bgcolor="#0a0d14",
    font=dict(color="#94a3b8", family="Inter"),
    title_x=0.5,
    title_font=dict(family="Cambria Math", size=15, color="#e2e8f0"),
    legend=dict(bgcolor="#111827", bordercolor="#1e2535", title="Semana"),
    bargap=0.25, margin=dict(t=45, b=20)
)
fig_sem.update_xaxes(gridcolor="#1e2535")
fig_sem.update_yaxes(gridcolor="#1e2535", title="Ativações")
st.plotly_chart(fig_sem, width="stretch")

st.markdown("---")

# ─── ABAS HISTÓRICAS ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Histórico de Leituras</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💧 Umidade & pH", "🌿 NPK", "🚿 Irrigação", "📊 Correlações"])

LAYOUT = dict(paper_bgcolor="#0a0d14", plot_bgcolor="#0a0d14",
              font=dict(color="#94a3b8", family="Cambria Math"))

with tab1:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Umidade do Solo (%)", "pH do Solo"),
                        vertical_spacing=0.12)
    fig.add_trace(go.Scatter(x=df_filtrado["timestamp"], y=df_filtrado["umidade"],
        mode="lines", name="Umidade", line=dict(color="#38bdf8", width=2),
        fill="tozeroy", fillcolor="rgba(56,189,248,0.07)"), row=1, col=1)
    fig.add_hline(y=60, line_dash="dash", line_color="#f59e0b", annotation_text="mín 60%", row=1, col=1)
    fig.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="máx 80%", row=1, col=1)
    fig.add_trace(go.Scatter(x=df_filtrado["timestamp"], y=df_filtrado["ph"],
        mode="lines", name="pH", line=dict(color="#a78bfa", width=2)), row=2, col=1)
    fig.add_hline(y=5.5, line_dash="dash", line_color="#f59e0b", annotation_text="5.5", row=2, col=1)
    fig.add_hline(y=7.0, line_dash="dash", line_color="#ef4444", annotation_text="7.0", row=2, col=1)
    fig.update_layout(height=450, showlegend=False, **LAYOUT)
    fig.update_xaxes(gridcolor="#1e2535")
    fig.update_yaxes(gridcolor="#1e2535")
    st.plotly_chart(fig, width="stretch")

with tab2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_filtrado["timestamp"], y=df_filtrado["nitrogenio"],
        mode="lines", name="N", line=dict(color="#4ade80", width=2)))
    fig2.add_trace(go.Scatter(x=df_filtrado["timestamp"], y=df_filtrado["fosforo"],
        mode="lines", name="P", line=dict(color="#fb923c", width=2)))
    fig2.add_trace(go.Scatter(x=df_filtrado["timestamp"], y=df_filtrado["potassio"],
        mode="lines", name="K", line=dict(color="#facc15", width=2)))
    fig2.add_hline(y=80,  line_dash="dot", line_color="#4ade80", annotation_text="N mín")
    fig2.add_hline(y=30,  line_dash="dot", line_color="#fb923c", annotation_text="P mín")
    fig2.add_hline(y=100, line_dash="dot", line_color="#facc15", annotation_text="K mín")
    fig2.update_layout(height=400, yaxis_title="mg/kg",
                       legend=dict(bgcolor="#111827", bordercolor="#1e2535"), **LAYOUT)
    fig2.update_xaxes(gridcolor="#1e2535")
    fig2.update_yaxes(gridcolor="#1e2535")
    st.plotly_chart(fig2, width="stretch")
    cn, cp, ck = st.columns(3)
    with cn:
        mn = df_filtrado["nitrogenio"].mean()
        st.metric("Média N", f"{mn:.1f} mg/kg", "✅ OK" if mn >= 80 else "⚠️ Baixo")
    with cp:
        mp = df_filtrado["fosforo"].mean()
        st.metric("Média P", f"{mp:.1f} mg/kg", "✅ OK" if mp >= 30 else "⚠️ Baixo")
    with ck:
        mk = df_filtrado["potassio"].mean()
        st.metric("Média K", f"{mk:.1f} mg/kg", "✅ OK" if mk >= 100 else "⚠️ Baixo")

with tab3:
    ca, cb = st.columns(2)
    with ca:
        id2 = df_filtrado.groupby("data")["irrigacao"].sum().reset_index()
        id2.columns = ["data", "ativacoes"]
        fig3 = px.bar(id2, x="data", y="ativacoes", title="Ativações por Dia",
                      color="ativacoes", color_continuous_scale=["#111827", "#4ade80"])
        fig3.update_layout(showlegend=False, coloraxis_showscale=False,
                           title_x=0.5, **LAYOUT)
        fig3.update_xaxes(gridcolor="#1e2535")
        fig3.update_yaxes(gridcolor="#1e2535")
        st.plotly_chart(fig3, width="stretch")
    with cb:
        total     = len(df_filtrado)
        irrigando = df_filtrado["irrigacao"].sum()
        com_chuva = df_filtrado["chuva"].sum()
        inativo   = max(total - irrigando - com_chuva, 0)
        fig4 = go.Figure(go.Pie(
            labels=["Irrigação Ativa", "Com Chuva", "Inativo"],
            values=[irrigando, com_chuva, inativo],
            hole=0.5, marker_colors=["#4ade80", "#38bdf8", "#475569"]
        ))
        fig4.update_layout(title="Distribuição dos Estados", title_x=0.5,
                           legend=dict(bgcolor="#111827"), **LAYOUT)
        st.plotly_chart(fig4, width="stretch")

with tab4:
    cx, cy = st.columns(2)
    with cx:
        eixo_x = st.selectbox("Eixo X", ["umidade","ph","nitrogenio","fosforo","potassio"], index=0)
    with cy:
        eixo_y = st.selectbox("Eixo Y", ["umidade","ph","nitrogenio","fosforo","potassio"], index=1)
    fig5 = px.scatter(df_filtrado, x=eixo_x, y=eixo_y,
        color=df_filtrado["irrigacao"].map({0:"Desligada", 1:"Ligada"}),
        color_discrete_map={"Ligada":"#4ade80","Desligada":"#ef4444"},
        title=f"Correlação: {eixo_x.capitalize()} × {eixo_y.capitalize()}",
        labels={"color":"Irrigação"})
    fig5.update_layout(title_x=0.5, legend=dict(bgcolor="#111827"), **LAYOUT)
    fig5.update_xaxes(gridcolor="#1e2535")
    fig5.update_yaxes(gridcolor="#1e2535")
    st.plotly_chart(fig5, width="stretch")

# ─── TABELA ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">📋 Dados Brutos</div>', unsafe_allow_html=True)
mostrar = st.slider("Últimos N registros", 10, len(df_filtrado), 20)
st.dataframe(
    df_filtrado.tail(mostrar).sort_values("timestamp", ascending=False),
    width="stretch", hide_index=True
)

# ─── RODAPÉ ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#334155; font-size:0.78rem;'>"
    "FarmTech Solutions © 2025 — FIAP Inteligência Artificial — Fase 3"
    "</p>",
    unsafe_allow_html=True
)