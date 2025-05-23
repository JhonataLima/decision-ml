import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Caminhos
DATA_PATH = "data/processed/dados_treinamento.pkl"
PIPELINE_PATH = "models/pipeline_transformacao.pkl"
MODEL_PATH = "models/random_forest_model.pkl"

def carregar_dados():
    print("Carregando dados de treino/teste...")
    X_train, X_test, y_train, y_test = joblib.load(DATA_PATH)

    # Remover linhas com NaN
    mask_train = ~np.isnan(X_train).any(axis=1)
    mask_test = ~np.isnan(X_test).any(axis=1)
    X_train, y_train = X_train[mask_train], y_train[mask_train]
    X_test, y_test = X_test[mask_test], y_test[mask_test]

    return X_train, X_test, y_train, y_test


def treinar_modelo(X_train, y_train):
    print("Treinando modelo RandomForestClassifier...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    return modelo


def avaliar_modelo(modelo, X_test, y_test):
    print("Avaliando modelo...")
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.4f}")
    print(classification_report(y_test, y_pred))


def salvar_modelo(modelo):
    print("Salvando modelo treinado...")
    joblib.dump(modelo, MODEL_PATH)


def main():
    X_train, X_test, y_train, y_test = carregar_dados()

    modelo = treinar_modelo(X_train, y_train)
    avaliar_modelo(modelo, X_test, y_test)
    salvar_modelo(modelo)
    print("\n✅ Treinamento finalizado com sucesso!")


if __name__ == "__main__":
    main()
