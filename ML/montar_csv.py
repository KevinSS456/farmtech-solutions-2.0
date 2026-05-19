import pandas as pd
from pathlib import Path


ENTRADA = Path("./ML/csvs/produtos_agricolas.csv")
SAIDA = Path("./ML/csvs/produtos_agricolas_ml.csv")

df = pd.read_csv(ENTRADA)

colunas_esperadas = [
    "N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"
]

df = df[colunas_esperadas]

colunas_numericas = [
    "N", "P", "K", "temperature", "humidity", "ph", "rainfall"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df["label"] = df["label"].astype(str).str.strip().str.lower()

df = df.dropna()
df = df.drop_duplicates()

df = df[df["N"] >= 0]
df = df[df["P"] >= 0]
df = df[df["K"] >= 0]
df = df[df["temperature"].between(0, 60)]
df = df[df["humidity"].between(0, 100)]
df = df[df["ph"].between(0, 14)]
df = df[df["rainfall"] >= 0]

df.to_csv(SAIDA, index=False)

print("CSV final salvo em:", SAIDA)
print(df.head())
print(df.info())
print(df["label"].value_counts())
