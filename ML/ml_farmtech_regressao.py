"""
FarmTech Solutions — Regressão para Previsão Agrícola
FIAP — Inteligência Artificial
"""

import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline


# ──────────────────────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────────────────────

CAMINHO_CSV  = "./dashboard/sensores_farmtech_v2.csv"
OUTPUT_DIR   = "./ML/outputs"
RANDOM_STATE = 42
TEST_SIZE    = 0.2
FEATURES     = ["nitrogenio", "fosforo", "potassio", "chuva", "hora", "dia"]

os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use("seaborn-v0_8-darkgrid")


# ──────────────────────────────────────────────────────────────
# 1. CARREGAMENTO E PRÉ-PROCESSAMENTO
# ──────────────────────────────────────────────────────────────

def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Features temporais extraídas do timestamp
    df["hora"] = df["timestamp"].dt.hour
    df["dia"]  = df["timestamp"].dt.day

    # Tratamento de nulos com mediana (boa prática mesmo sem nulos)
    if df.isnull().sum().sum() > 0:
        df.fillna(df.median(numeric_only=True), inplace=True)

    # Remoção de duplicatas
    df = df.drop_duplicates().reset_index(drop=True)

    # Feature de rendimento estimado (índice agronômico 0–100)
    # Ponderação baseada nos limiares definidos nas fases anteriores
    df["rendimento"] = (
        0.30 * (df["nitrogenio"] / 140).clip(0, 1) +
        0.20 * (df["fosforo"]   / 145).clip(0, 1) +
        0.20 * (df["potassio"]  / 205).clip(0, 1) +
        0.20 * ((df["umidade"] - 60).clip(0) / 35).clip(0, 1) +
        0.10 * ((df["ph"] - 5.5) / 1.5).clip(0, 1)
    ) * 100

    df["rendimento"] = df["rendimento"].clip(0, 100).round(2)

    return df


# ──────────────────────────────────────────────────────────────
# 2. SEPARAÇÃO TREINO / TESTE
# ──────────────────────────────────────────────────────────────

def separar_treino_teste(df, target_col):
    X = df[FEATURES]
    y = df[target_col]

    return train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )


# ──────────────────────────────────────────────────────────────
# 3. MODELOS
# ──────────────────────────────────────────────────────────────

def treinar_random_forest(X_train, y_train):
    modelo = Pipeline([
        ("scaler", StandardScaler()),
        ("model",  RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=2,
            random_state=RANDOM_STATE
        ))
    ])

    modelo.fit(X_train, y_train)

    return modelo


def treinar_regressao_linear(X_train, y_train):
    modelo = Pipeline([
        ("scaler", StandardScaler()),
        ("model",  LinearRegression())
    ])

    modelo.fit(X_train, y_train)

    return modelo


def treinar_regressao_polinomial(X_train, y_train):
    # Regressão polinomial grau 2 com Ridge para evitar overfitting
    modelo = Pipeline([
        ("scaler", StandardScaler()),
        ("poly",   PolynomialFeatures(degree=2, include_bias=False)),
        ("model",  Ridge(alpha=1.0))
    ])

    modelo.fit(X_train, y_train)

    return modelo


# ──────────────────────────────────────────────────────────────
# 4. AVALIAÇÃO
# ──────────────────────────────────────────────────────────────

def avaliar_modelo(nome, y_test, y_pred):
    mae  = mean_absolute_error(y_test, y_pred)
    mse  = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_test, y_pred)

    print("\n" + "=" * 60)
    print(nome)
    print("=" * 60)

    print(f"MAE  (Erro Médio Absoluto):        {mae:.4f}")
    print(f"MSE  (Erro Quadrático Médio):       {mse:.4f}")
    print(f"RMSE (Raiz do Erro Quadrático):     {rmse:.4f}")
    print(f"R²   (Coeficiente de Determinação): {r2:.4f}")

    return {
        "modelo": nome,
        "MAE":    mae,
        "MSE":    mse,
        "RMSE":   rmse,
        "R2":     r2
    }


def validacao_cruzada(modelo, df, target_col):
    X = df[FEATURES]
    y = df[target_col]

    scores = cross_val_score(modelo, X, y, cv=5, scoring="r2")

    print(f"\nValidação Cruzada (5 folds) — R²: {scores.mean():.4f} ± {scores.std():.4f}")

    return scores


# ──────────────────────────────────────────────────────────────
# 5. GRÁFICOS
# ──────────────────────────────────────────────────────────────

def gerar_correlacao(df):
    fig, ax = plt.subplots(figsize=(9, 7))

    colunas = ["umidade", "ph", "nitrogenio", "fosforo",
               "potassio", "chuva", "irrigacao", "rendimento"]

    corr = df[colunas].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="RdYlGn", center=0, ax=ax,
        linewidths=0.5, annot_kws={"size": 10}
    )

    ax.set_title(
        "Mapa de Correlação — Variáveis do Solo",
        fontsize=14, fontweight="bold", pad=15
    )

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_correlacao.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 01_correlacao.png")


def gerar_predito_vs_real(resultados_graficos):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "Valores Preditos vs Reais — Random Forest",
        fontsize=14, fontweight="bold"
    )

    cores = ["#2ecc71", "#3498db", "#e74c3c"]

    for idx, (label, y_test, y_pred) in enumerate(resultados_graficos):
        ax = axes[idx]

        ax.scatter(y_test, y_pred, alpha=0.6, color=cores[idx],
                   edgecolors="white", s=60)

        lims = [
            min(y_test.min(), y_pred.min()) - 1,
            max(y_test.max(), y_pred.max()) + 1
        ]
        ax.plot(lims, lims, "k--", linewidth=1.5, label="Ideal (y=x)")
        ax.set_xlabel(f"Real — {label}", fontsize=9)
        ax.set_ylabel("Predito", fontsize=9)
        ax.set_title(f"{label}\nR² = {r2_score(y_test, y_pred):.3f}", fontsize=10)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_predito_vs_real.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 02_predito_vs_real.png")


def gerar_residuos(resultados_graficos):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "Análise de Resíduos — Random Forest",
        fontsize=14, fontweight="bold"
    )

    cores = ["#2ecc71", "#3498db", "#e74c3c"]

    for idx, (label, y_test, y_pred) in enumerate(resultados_graficos):
        ax    = axes[idx]
        resid = y_test.values - y_pred

        ax.scatter(y_pred, resid, alpha=0.6, color=cores[idx],
                   edgecolors="white", s=60)
        ax.axhline(0, color="black", linewidth=1.5, linestyle="--")
        ax.set_xlabel("Predito", fontsize=9)
        ax.set_ylabel("Resíduo (Real − Predito)", fontsize=9)
        ax.set_title(label, fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_residuos.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 03_residuos.png")


def gerar_comparacao_modelos(todos_resultados):
    labels  = list({r["modelo"].split("—")[0].strip() for r in todos_resultados})
    targets = ["Umidade", "pH", "Rendimento"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        "Comparação de Modelos por Target",
        fontsize=13, fontweight="bold"
    )

    cores   = ["#2ecc71", "#3498db", "#e74c3c"]
    modelos = ["Random Forest", "Linear", "Polinomial"]
    x       = np.arange(len(targets))
    width   = 0.25

    for mi, metrica in enumerate(["RMSE", "R2"]):
        ax = axes[mi]

        for i, modelo in enumerate(modelos):
            vals = [
                r[metrica] for r in todos_resultados
                if modelo in r["modelo"]
            ]
            if vals:
                bars = ax.bar(
                    x + (i - 1) * width, vals, width,
                    label=modelo, color=cores[i], alpha=0.85
                )
                ax.bar_label(bars, fmt="%.2f", fontsize=7, padding=2)

        ax.set_xticks(x)
        ax.set_xticklabels(targets, fontsize=9)
        ax.set_title(metrica, fontsize=12)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_comparacao_modelos.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 04_comparacao_modelos.png")


def gerar_feature_importance(modelo_umidade):
    if not hasattr(modelo_umidade.named_steps.get("model"), "feature_importances_"):
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    importances = modelo_umidade.named_steps["model"].feature_importances_
    feat_series = pd.Series(importances, index=FEATURES).sort_values(ascending=True)

    feat_series.plot(kind="barh", ax=ax, color="#2ecc71", alpha=0.85, edgecolor="white")

    ax.set_title(
        "Importância das Features — Modelo de Umidade (RF)",
        fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Importância Relativa", fontsize=11)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 05_feature_importance.png")


def gerar_serie_temporal(df, modelo_umidade):
    fig, ax = plt.subplots(figsize=(14, 5))

    umidade_pred = modelo_umidade.predict(df[FEATURES])

    ax.plot(df["timestamp"], df["umidade"],
            label="Real", color="#3498db", linewidth=1.5, alpha=0.8)
    ax.plot(df["timestamp"], umidade_pred,
            label="Predito", color="#2ecc71", linewidth=1.5, linestyle="--")
    ax.axhspan(60, 80, alpha=0.12, color="green", label="Faixa ideal (60–80%)")

    ax.set_title(
        "Série Temporal — Umidade Real vs Predita",
        fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Umidade (%)")
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/06_serie_temporal_umidade.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 06_serie_temporal_umidade.png")


def gerar_tendencia_rendimento(df, modelo_rendimento):
    fig, ax = plt.subplots(figsize=(14, 5))

    rend_pred = modelo_rendimento.predict(df[FEATURES])

    ax.fill_between(df["timestamp"], df["rendimento"],
                    alpha=0.3, color="#f39c12", label="Real")
    ax.fill_between(df["timestamp"], rend_pred,
                    alpha=0.3, color="#e74c3c", label="Predito")

    ax.plot(df["timestamp"], df["rendimento"],
            color="#f39c12", linewidth=1.2)
    ax.plot(df["timestamp"], rend_pred,
            color="#e74c3c", linewidth=1.2, linestyle="--")

    ax.axhline(70, color="green", linewidth=1,
               linestyle=":", label="Meta de rendimento (70)")

    ax.set_title(
        "Tendência de Rendimento Estimado — Janeiro 2025",
        fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Rendimento (0–100)")
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/07_tendencia_rendimento.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 07_tendencia_rendimento.png")


def gerar_histograma_residuos(resultados_graficos):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        "Distribuição dos Resíduos — Random Forest",
        fontsize=13, fontweight="bold"
    )

    cores = ["#2ecc71", "#3498db", "#e74c3c"]

    for idx, (label, y_test, y_pred) in enumerate(resultados_graficos):
        ax    = axes[idx]
        resid = y_test.values - y_pred

        ax.hist(resid, bins=20, color=cores[idx], alpha=0.8, edgecolor="white")
        ax.axvline(0, color="black", linewidth=2, linestyle="--")
        ax.axvline(resid.mean(), color="red", linewidth=1.5,
                   label=f"Média: {resid.mean():.2f}")

        ax.set_title(label, fontsize=10)
        ax.set_xlabel("Resíduo")
        ax.set_ylabel("Frequência")
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/08_histograma_residuos.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("   ✅ 08_histograma_residuos.png")


# ──────────────────────────────────────────────────────────────
# 6. RECOMENDAÇÕES
# ──────────────────────────────────────────────────────────────

def recomendar(modelos, nitrogenio, fosforo, potassio, chuva, hora=9, dia=15):
    """
    Recebe leituras dos sensores e retorna recomendações
    baseadas nas previsões dos modelos treinados.
    """
    entrada = pd.DataFrame(
        [[nitrogenio, fosforo, potassio, chuva, hora, dia]],
        columns=FEATURES
    )

    umidade_pred    = modelos["umidade"].predict(entrada)[0]
    ph_pred         = modelos["ph"].predict(entrada)[0]
    rendimento_pred = modelos["rendimento"].predict(entrada)[0]

    recomendacoes = []

    # Irrigação
    if chuva == 1:
        recomendacoes.append("🌧️  Chuva prevista — SUSPENDER irrigação")
    elif umidade_pred < 60:
        volume = round((60 - umidade_pred) * 0.8, 1)
        recomendacoes.append(
            f"💧 Solo seco ({umidade_pred:.1f}%) — IRRIGAR | Volume estimado: {volume} L/m²"
        )
    elif umidade_pred > 80:
        recomendacoes.append(f"⚠️  Solo encharcado ({umidade_pred:.1f}%) — NÃO irrigar")
    else:
        recomendacoes.append(f"✅ Umidade adequada ({umidade_pred:.1f}%) — Irrigação desnecessária")

    # pH
    if ph_pred < 6.0:
        recomendacoes.append(f"🧪 pH baixo ({ph_pred:.2f}) — Aplicar calcário dolomítico")
    elif ph_pred > 6.5:
        recomendacoes.append(f"🧪 pH alto ({ph_pred:.2f}) — Aplicar enxofre agrícola")
    else:
        recomendacoes.append(f"✅ pH ideal ({ph_pred:.2f}) — Nenhuma correção necessária")

    # NPK
    if nitrogenio < 80:
        recomendacoes.append(f"🌿 N baixo ({nitrogenio} mg/kg) — Aplicar ureia ou nitrato de amônio")
    if fosforo < 30:
        recomendacoes.append(f"🌿 P baixo ({fosforo} mg/kg) — Aplicar superfosfato simples")
    if potassio < 100:
        recomendacoes.append(f"🌿 K baixo ({potassio} mg/kg) — Aplicar cloreto de potássio")
    if nitrogenio >= 80 and fosforo >= 30 and potassio >= 100:
        recomendacoes.append("✅ NPK adequado — Sem necessidade de fertilização")

    # Rendimento
    if rendimento_pred >= 70:
        nivel = "🟢 Alto"
    elif rendimento_pred >= 40:
        nivel = "🟡 Médio"
    else:
        nivel = "🔴 Baixo"

    recomendacoes.append(f"📈 Rendimento estimado: {rendimento_pred:.1f}/100 — {nivel}")

    return {
        "umidade_prevista":    round(float(umidade_pred), 2),
        "ph_previsto":         round(float(ph_pred), 3),
        "rendimento_previsto": round(float(rendimento_pred), 2),
        "recomendacoes":       recomendacoes,
    }


# ──────────────────────────────────────────────────────────────
# 7. EXPORTAÇÕES
# ──────────────────────────────────────────────────────────────

def exportar_metricas(todos_resultados):
    df_metrics = pd.DataFrame(todos_resultados)
    df_metrics.to_csv(f"{OUTPUT_DIR}/metricas_modelos.csv", index=False)

    print(f"\n✅ metricas_modelos.csv exportado")


def exportar_previsoes(df, modelos):
    df_export = df[["timestamp"] + FEATURES + ["umidade", "ph", "rendimento"]].copy()

    df_export["umidade_pred"]    = modelos["umidade"].predict(df[FEATURES]).round(2)
    df_export["ph_pred"]         = modelos["ph"].predict(df[FEATURES]).round(3)
    df_export["rendimento_pred"] = modelos["rendimento"].predict(df[FEATURES]).round(2)

    df_export.to_csv(f"{OUTPUT_DIR}/previsoes_farmtech.csv", index=False)

    print(f"✅ previsoes_farmtech.csv exportado")


def exportar_modelos(modelos):
    joblib.dump(modelos, f"{OUTPUT_DIR}/todos_modelos.pkl")

    print(f"✅ todos_modelos.pkl exportado")


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    todos_resultados   = []
    modelos_salvos     = {}
    resultados_graficos = []  # (label, y_test, y_pred_rf) por target

    # ── Carregamento
    print("=" * 60)
    print("FARMTECH — PIPELINE DE REGRESSÃO")
    print("=" * 60)

    df = carregar_dados()

    print(f"\nDataset carregado: {len(df)} registros")
    print(f"Período: {df['timestamp'].min().date()} → {df['timestamp'].max().date()}")
    print(f"Nulos  : {df.isnull().sum().sum()} ✅")

    # ── Targets
    targets = {
        "umidade":    "Umidade do Solo (%)",
        "ph":         "pH do Solo",
        "rendimento": "Rendimento Estimado (0–100)",
    }

    # ── Treinamento e avaliação por target
    for target_col, target_label in targets.items():
        print("\n" + "=" * 60)
        print(f"TARGET: {target_label}")
        print("=" * 60)

        X_train, X_test, y_train, y_test = separar_treino_teste(df, target_col)

        # Treina os 3 modelos
        modelo_rf   = treinar_random_forest(X_train, y_train)
        modelo_lin  = treinar_regressao_linear(X_train, y_train)
        modelo_poly = treinar_regressao_polinomial(X_train, y_train)

        y_pred_rf   = modelo_rf.predict(X_test)
        y_pred_lin  = modelo_lin.predict(X_test)
        y_pred_poly = modelo_poly.predict(X_test)

        # Avalia
        r_rf   = avaliar_modelo(f"RANDOM FOREST — {target_label}",   y_test, y_pred_rf)
        r_lin  = avaliar_modelo(f"REGRESSÃO LINEAR — {target_label}", y_test, y_pred_lin)
        r_poly = avaliar_modelo(f"REGRESSÃO POLINOMIAL — {target_label}", y_test, y_pred_poly)

        # Validação cruzada no melhor modelo (RF)
        validacao_cruzada(modelo_rf, df, target_col)

        todos_resultados.extend([r_rf, r_lin, r_poly])

        # Escolhe o melhor modelo por R²
        melhor = max(
            [("Random Forest", modelo_rf, r_rf),
             ("Linear",        modelo_lin,  r_lin),
             ("Polinomial",    modelo_poly, r_poly)],
            key=lambda x: x[2]["R2"]
        )

        print(f"\n✅ Melhor modelo para {target_label}: {melhor[0]} (R²: {melhor[2]['R2']:.4f})")

        modelos_salvos[target_col] = melhor[1]
        resultados_graficos.append((target_label, y_test, y_pred_rf))

    # ── Comparação final
    print("\n" + "=" * 60)
    print("COMPARAÇÃO FINAL — R² POR MODELO E TARGET")
    print("=" * 60)

    for r in todos_resultados:
        print(f"{r['modelo']}: R²={r['R2']:.4f} | RMSE={r['RMSE']:.4f} | MAE={r['MAE']:.4f}")

    # ── Gráficos
    print("\n" + "=" * 60)
    print("GERANDO GRÁFICOS")
    print("=" * 60)

    gerar_correlacao(df)
    gerar_predito_vs_real(resultados_graficos)
    gerar_residuos(resultados_graficos)
    gerar_comparacao_modelos(todos_resultados)
    gerar_feature_importance(modelos_salvos["umidade"])
    gerar_serie_temporal(df, modelos_salvos["umidade"])
    gerar_tendencia_rendimento(df, modelos_salvos["rendimento"])
    gerar_histograma_residuos(resultados_graficos)

    # ── Exportações
    print("\n" + "=" * 60)
    print("EXPORTANDO ARQUIVOS")
    print("=" * 60)

    exportar_metricas(todos_resultados)
    exportar_previsoes(df, modelos_salvos)
    exportar_modelos(modelos_salvos)

    # ── Recomendações
    print("\n" + "=" * 60)
    print("RECOMENDAÇÕES DE IRRIGAÇÃO E MANEJO")
    print("=" * 60)

    cenarios = [
        {"nitrogenio": 55,  "fosforo": 20, "potassio": 85,  "chuva": 0, "nome": "Solo deficiente"},
        {"nitrogenio": 100, "fosforo": 50, "potassio": 120, "chuva": 1, "nome": "Solo rico + chuva"},
        {"nitrogenio": 90,  "fosforo": 40, "potassio": 110, "chuva": 0, "nome": "Condições ideais"},
    ]

    for c in cenarios:
        r = recomendar(modelos_salvos, c["nitrogenio"], c["fosforo"], c["potassio"], c["chuva"])

        print(f"\nCenário: {c['nome']}")
        print(f"  Umidade: {r['umidade_prevista']}% | pH: {r['ph_previsto']} | Rendimento: {r['rendimento_previsto']}/100")
        print("  Recomendações:")

        for msg in r["recomendacoes"]:
            print(f"    {msg}")

    print("\n" + "=" * 60)
    print("PIPELINE CONCLUÍDO COM SUCESSO ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()
