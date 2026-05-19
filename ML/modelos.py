from pipeline import preparar_dataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


CAMINHO_CSV = "./ML/csvs/produtos_agricolas_ml.csv"


def carregar_dados():
    df = preparar_dataset(CAMINHO_CSV)

    X = df.drop(columns=["label"])
    y = df["label"]

    return X, y


def separar_treino_teste(X, y):
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def aplicar_scaler(X_train, X_test):
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled


def avaliar_modelo(nome, y_test, y_pred):
    acc = accuracy_score(y_test, y_pred)

    print("\n" + "=" * 60)
    print(nome)
    print("=" * 60)

    print("Accuracy:", acc)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    return {
        "modelo": nome,
        "accuracy": acc
    }


def treinar_logistic(X_train_scaled, y_train):
    modelo = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    modelo.fit(X_train_scaled, y_train)

    return modelo


def treinar_random_forest(X_train, y_train):
    modelo = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    modelo.fit(X_train, y_train)

    return modelo


def treinar_decision_tree(X_train, y_train):
    modelo = DecisionTreeClassifier(
        max_depth=8,
        random_state=42
    )

    modelo.fit(X_train, y_train)

    return modelo


def treinar_svm(X_train_scaled, y_train):
    modelo = SVC(
        kernel="rbf",
        probability=True,
        random_state=42
    )

    modelo.fit(X_train_scaled, y_train)

    return modelo


def treinar_knn(X_train_scaled, y_train):
    modelo = KNeighborsClassifier(
        n_neighbors=5
    )

    modelo.fit(X_train_scaled, y_train)

    return modelo


def main():
    resultados = []

    X, y = carregar_dados()

    X_train, X_test, y_train, y_test = separar_treino_teste(
        X,
        y
    )

    X_train_scaled, X_test_scaled = aplicar_scaler(
        X_train,
        X_test
    )

    # Logistic Regression
    modelo_log = treinar_logistic(
        X_train_scaled,
        y_train
    )

    y_pred_log = modelo_log.predict(
        X_test_scaled
    )

    resultados.append(
        avaliar_modelo(
            "LOGISTIC REGRESSION",
            y_test,
            y_pred_log
        )
    )

    # Random Forest
    modelo_rf = treinar_random_forest(
        X_train,
        y_train
    )

    y_pred_rf = modelo_rf.predict(
        X_test
    )

    resultados.append(
        avaliar_modelo(
            "RANDOM FOREST",
            y_test,
            y_pred_rf
        )
    )

    # Decision Tree
    modelo_dt = treinar_decision_tree(
        X_train,
        y_train
    )

    y_pred_dt = modelo_dt.predict(
        X_test
    )

    resultados.append(
        avaliar_modelo(
            "DECISION TREE",
            y_test,
            y_pred_dt
        )
    )

    # SVM
    modelo_svm = treinar_svm(
        X_train_scaled,
        y_train
    )

    y_pred_svm = modelo_svm.predict(
        X_test_scaled
    )

    resultados.append(
        avaliar_modelo(
            "SVM",
            y_test,
            y_pred_svm
        )
    )

    # KNN
    modelo_knn = treinar_knn(
        X_train_scaled,
        y_train
    )

    y_pred_knn = modelo_knn.predict(
        X_test_scaled
    )

    resultados.append(
        avaliar_modelo(
            "KNN",
            y_test,
            y_pred_knn
        )
    )

    print("\n" + "=" * 60)
    print("COMPARAÇÃO FINAL")
    print("=" * 60)

    for resultado in sorted(
        resultados,
        key=lambda x: x["accuracy"],
        reverse=True
    ):
        print(
            f"{resultado['modelo']}: "
            f"{resultado['accuracy']:.4f}"
        )


if __name__ == "__main__":
    main()
