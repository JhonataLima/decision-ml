import pandas as pd
import joblib
import os
from features.feature_selection import label_encode_df

PIPELINE_PATH = "models/pipeline_transformacao.pkl"
MODEL_PATH = "models/random_forest_model.pkl"
NOVOS_DADOS_PATH = "data/inference/dados_testes.csv"
OUTPUT_PATH = "data/inference/predicoes.csv"

COLUNAS_ESPERADAS = [
    'informacoes_profissionais_nivel_profissional',
    'informacoes_profissionais_area_atuacao',
    'formacao_e_idiomas_nivel_academico',
    'formacao_e_idiomas_nivel_ingles',
    'formacao_e_idiomas_nivel_espanhol',
    'formacao_e_idiomas_ano_conclusao'
]

def carregar_pipeline_e_modelo():
    print("🔄 Carregando pipeline e modelo...")
    pipeline = joblib.load(PIPELINE_PATH)
    modelo = joblib.load(MODEL_PATH)
    return pipeline, modelo

def carregar_dados():
    print(f"📥 Lendo novos dados de '{NOVOS_DADOS_PATH}'...")
    return pd.read_csv(NOVOS_DADOS_PATH)

def preparar_dados(df):
    print("🧹 Tratando colunas faltantes e extras...")

    df = df[[col for col in df.columns if col in COLUNAS_ESPERADAS]]

    for col in COLUNAS_ESPERADAS:
        if col not in df.columns:
            df[col] = None

    df = df[COLUNAS_ESPERADAS]
    return df

def salvar_predicoes(predicoes):
    print(f"💾 Salvando previsões em '{OUTPUT_PATH}'...")
    predicoes.to_csv(OUTPUT_PATH, index=False)

def main():
    pipeline, modelo = carregar_pipeline_e_modelo()
    novos_dados = carregar_dados()

    dados_preparados = preparar_dados(novos_dados)
    dados_transformados = pipeline.transform(dados_preparados)

    print("🤖 Realizando inferência...")
    resultados = modelo.predict(dados_transformados)
    df_resultados = novos_dados.copy()
    df_resultados["predicao"] = resultados

    salvar_predicoes(df_resultados)
    print("\n✅ Inferência finalizada com sucesso!")

if __name__ == "__main__":
    main()
