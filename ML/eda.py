import matplotlib.pyplot as plt
import seaborn as sns

from pipeline import preparar_dataset

df = preparar_dataset(
    "./ML/csvs/produtos_agricolas_ml.csv"
)

sns.set_theme(style="whitegrid")

# gráfico 1 — distribuição das culturas
plt.figure(figsize=(14, 6))

sns.countplot(
    data=df,
    x="label",
    order=df["label"].value_counts().index
)

plt.title("Distribuição das culturas")
plt.xticks(rotation=45)

plt.show()

# gráfico 2: histograma temperatura
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="temperature",
    bins=30,
    kde=True
)

plt.title("Distribuição da temperatura")

plt.show()

# gráfico 3 — histograma pH
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="ph",
    bins=30,
    kde=True
)

plt.title("Distribuição do pH")

plt.show()

# gráfico 4 — scatter
plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="humidity",
    y="rainfall",
    hue="label"
)

plt.title("Humidity vs Rainfall")

plt.show()

# gráfico 5 — heatmap
plt.figure(figsize=(10, 8))

sns.heatmap(
    df.drop(columns=["label"]).corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlação entre variáveis")

plt.show()

# gráfico 6 — boxplot por cultura
culturas = df["label"].value_counts().head(5).index

df_top = df[df["label"].isin(culturas)]

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=df_top,
    x="label",
    y="ph"
)

plt.title("pH por cultura")

plt.show()


# Pedido: perfil ideal de 3 culturas
culturas = ["rice", "banana", "maize"]

for cultura in culturas:
    print("\n" + "=" * 60)
    print(f"CULTURA: {cultura}")

    dados = df[df["label"] == cultura]

    medias = dados[
        [
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]
    ].mean()

    print(medias)
