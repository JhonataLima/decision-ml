import pandas as pd
import joblib
import os
import numpy as np
from src.model.custom_transformers import label_encode_df

PIPELINE_PATH = "models/pipeline_transformacao.pkl"
MODEL_PATH = "models/random_forest_model.pkl"
NOVOS_DADOS_PATH = "data/inference/dados_testes.csv"
OUTPUT_PATH = "data/inference/predicoes.csv"

# Colunas esperadas pelo pipeline (incluindo derivadas)
COLUNAS_ESPERADAS = [
    'modalidade',
    'valor_venda',
    'titulo_vaga',
    'cliente',
    'requisitante',
    'analista_responsavel',
    'infos_basicas_objetivo_profissional',
    'infos_basicas_local',
    'infos_basicas_sabendo_de_nos_por',
    'informacoes_pessoais_sexo',
    'informacoes_pessoais_estado_civil',
    'informacoes_pessoais_pcd',
    'informacoes_profissionais_area_atuacao',
    'informacoes_profissionais_titulo_profissional',
    'informacoes_profissionais_remuneracao',
    'informacoes_profissionais_nivel_profissional',
    'formacao_e_idiomas_nivel_academico',
    'formacao_e_idiomas_nivel_ingles',
    'formacao_e_idiomas_nivel_espanhol',
    'cargo_atual_cargo_atual',
    'cargo_atual_cliente',
    'cargo_atual_unidade',
    'idade',
    'anos_na_empresa'
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
    print("🧹 Tratando colunas faltantes, extras e calculando derivadas...")

    # Calcular idade se possível
    if 'informacoes_pessoais_data_nascimento' in df.columns:
        df['informacoes_pessoais_data_nascimento'] = pd.to_datetime(df['informacoes_pessoais_data_nascimento'], errors='coerce')
        df['idade'] = pd.Timestamp.now().year - df['informacoes_pessoais_data_nascimento'].dt.year
    else:
        df['idade'] = np.nan

    # Calcular anos_na_empresa se possível
    if 'cargo_atual_data_admissao' in df.columns:
        df['cargo_atual_data_admissao'] = pd.to_datetime(df['cargo_atual_data_admissao'], errors='coerce')
        df['anos_na_empresa'] = pd.Timestamp.now().year - df['cargo_atual_data_admissao'].dt.year
    else:
        df['anos_na_empresa'] = np.nan

    # Adicionar colunas faltantes como NaN
    for col in COLUNAS_ESPERADAS:
        if col not in df.columns:
            df[col] = np.nan

    # Garante a ordem das colunas
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