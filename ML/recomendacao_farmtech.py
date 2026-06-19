"""
FarmTech Solutions - Sistema de Recomendação de Manejo Agrícola
Integrante 4 - Lógica de sugestão de ações baseada nas previsões do modelo de regressão
"""

import pandas as pd
from pathlib import Path

CAMINHO_CSV = Path(__file__).parent / "outputs" / "previsoes_farmtech.csv"


def gerar_recomendacoes(linha):
    """Recebe uma linha do dataset (com valores previstos) e retorna lista de recomendações."""
    recomendacoes = []

    # --- Umidade ---
    if linha["umidade_pred"] < 60:
        volume = round((60 - linha["umidade_pred"]) * 0.5, 1)  # estimativa simples de L/m²
        recomendacoes.append(f"💧 IRRIGAR — umidade prevista em {linha['umidade_pred']:.1f}% (abaixo de 60%). Volume estimado: {volume} L/m²")
    elif linha["umidade_pred"] > 80:
        recomendacoes.append(f"⚠️ NÃO IRRIGAR — umidade prevista em {linha['umidade_pred']:.1f}% (solo encharcado)")
    else:
        recomendacoes.append(f"✅ Umidade prevista em {linha['umidade_pred']:.1f}% — dentro da faixa ideal")

    # --- Chuva ---
    if linha["chuva"] == 1:
        recomendacoes.append("🌧️ SUSPENDER IRRIGAÇÃO — chuva prevista")

    # --- pH ---
    if linha["ph_pred"] < 6.0:
        recomendacoes.append(f"🧪 APLICAR CALCÁRIO DOLOMÍTICO — pH previsto em {linha['ph_pred']:.2f} (abaixo de 6.0)")
    elif linha["ph_pred"] > 6.5:
        recomendacoes.append(f"🧪 APLICAR ENXOFRE AGRÍCOLA — pH previsto em {linha['ph_pred']:.2f} (acima de 6.5)")
    else:
        recomendacoes.append(f"✅ pH previsto em {linha['ph_pred']:.2f} — dentro da faixa ideal")

    # --- NPK ---
    if linha["nitrogenio"] < 80:
        recomendacoes.append(f"🌿 APLICAR UREIA / NITRATO DE AMÔNIO — Nitrogênio em {linha['nitrogenio']:.1f} mg/kg (mínimo: 80)")
    if linha["fosforo"] < 30:
        recomendacoes.append(f"🌿 APLICAR SUPERFOSFATO SIMPLES — Fósforo em {linha['fosforo']:.1f} mg/kg (mínimo: 30)")
    if linha["potassio"] < 100:
        recomendacoes.append(f"🌿 APLICAR CLORETO DE POTÁSSIO — Potássio em {linha['potassio']:.1f} mg/kg (mínimo: 100)")

    # --- Rendimento estimado ---
    if linha["rendimento_pred"] < 50:
        recomendacoes.append(f"🌾 ATENÇÃO — rendimento estimado em {linha['rendimento_pred']:.1f} (abaixo do esperado). Revisar manejo geral.")
    else:
        recomendacoes.append(f"🌾 Rendimento estimado em {linha['rendimento_pred']:.1f} — dentro do esperado")

    return recomendacoes


def main():
    df = pd.read_csv(CAMINHO_CSV, parse_dates=["timestamp"])

    print("=" * 60)
    print(" FarmTech Solutions — Sistema de Recomendação de Manejo")
    print("=" * 60)

    ultima_leitura = df.iloc[-1]

    print(f"\nLeitura: {ultima_leitura['timestamp']}")
    print(f"Nitrogênio: {ultima_leitura['nitrogenio']:.1f} mg/kg | "
          f"Fósforo: {ultima_leitura['fosforo']:.1f} mg/kg | "
          f"Potássio: {ultima_leitura['potassio']:.1f} mg/kg")
    print(f"Umidade prevista: {ultima_leitura['umidade_pred']:.1f}% | "
          f"pH previsto: {ultima_leitura['ph_pred']:.2f} | "
          f"Rendimento previsto: {ultima_leitura['rendimento_pred']:.1f}")

    print("\n--- RECOMENDAÇÕES ---\n")
    for r in gerar_recomendacoes(ultima_leitura):
        print(r)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()