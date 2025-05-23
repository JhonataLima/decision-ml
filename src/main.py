from features.feature_selection import main as feature_selection_main
from model.classificacao import (
    carregar_dados,
    treinar_modelo,
    avaliar_modelo,
    salvar_modelo
)

def main():
    print("🚀 Iniciando pipeline...")

    # 1. Seleção e transformação de features
    print("📥 Selecionando e transformando features...")
    feature_selection_main()  # Gera os arquivos de treino/teste e pipeline

    # 2. Carregar dados processados
    print("📦 Carregando dados processados...")
    X_train, X_test, y_train, y_test = carregar_dados()

    # 3. Treinamento do modelo
    print("🤖 Treinando modelo...")
    modelo = treinar_modelo(X_train, y_train)

    # 4. Avaliação
    print("📊 Avaliando modelo...")
    avaliar_modelo(modelo, X_test, y_test)

    # 5. Salvar modelo treinado
    print("💾 Salvando modelo treinado...")
    salvar_modelo(modelo)

    print("✅ Pipeline finalizada com sucesso!")

if __name__ == "__main__":
    main()