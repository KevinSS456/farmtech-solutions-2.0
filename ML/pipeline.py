import pandas as pd


COLUNAS_NUMERICAS = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]


COLUNA_TARGET = "label"


def carregar_dataset(caminho):
    df = pd.read_csv(caminho)
    return df


def diagnostico(df):
    print("=" * 60)
    print("HEAD")
    print(df.head())

    print("\n" + "=" * 60)
    print("INFO")
    print(df.info())

    print("\n" + "=" * 60)
    print("NULLS")
    print(df.isnull().sum())

    print("\n" + "=" * 60)
    print("DESCRIBE")
    print(df.describe())

    print("\n" + "=" * 60)
    print("LABELS")
    print(df["label"].value_counts())


def normalizar_tipos(df):
    df = df.copy()

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    df[COLUNA_TARGET] = (
        df[COLUNA_TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return df


def tratar_nulos(df):
    df = df.copy()

    for coluna in COLUNAS_NUMERICAS:
        mediana = df[coluna].median()

        df[coluna] = df[coluna].fillna(
            mediana
        )

    df = df.dropna(subset=[COLUNA_TARGET])

    return df


def remover_duplicados(df):
    return df.drop_duplicates()


def filtrar_regras(df):
    df = df.copy()

    df = df[df["N"] >= 0]
    df = df[df["P"] >= 0]
    df = df[df["K"] >= 0]

    df = df[df["temperature"].between(0, 60)]
    df = df[df["humidity"].between(0, 100)]
    df = df[df["ph"].between(0, 14)]
    df = df[df["rainfall"] >= 0]

    return df


def preparar_dataset(caminho):
    df = carregar_dataset(caminho)

    df = normalizar_tipos(df)

    df = tratar_nulos(df)

    df = remover_duplicados(df)

    df = filtrar_regras(df)

    return df


if __name__ == "__main__":
    df = preparar_dataset('./ML/csvs/produtos_agricolas_ml.csv')
    diagnostico(df)
