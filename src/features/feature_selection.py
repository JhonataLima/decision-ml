import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import os

def calcular_idade(data_nascimento):
    if pd.isnull(data_nascimento):
        return np.nan
    return pd.Timestamp.now().year - data_nascimento.year

def carregar_base(path="data/processed/feature_engineering.parquet"):
    return pd.read_parquet(path)

def selecionar_e_transformar(df):
    colunas = [
        # Pessoais
        'informacoes_pessoais_data_nascimento', 'informacoes_pessoais_sexo',
        'informacoes_pessoais_estado_civil', 'informacoes_pessoais_pcd',
        'infos_basicas_local', 'infos_basicas_sabendo_de_nos_por',
        'informacoes_pessoais_fonte_indicacao',
        # Formação
        'formacao_e_idiomas_nivel_academico', 'formacao_e_idiomas_nivel_ingles',
        'formacao_e_idiomas_nivel_espanhol', 'formacao_e_idiomas_outro_idioma',
        'formacao_e_idiomas_cursos',
        # Profissionais
        'informacoes_profissionais_area_atuacao',
        'informacoes_profissionais_nivel_profissional',
        'informacoes_profissionais_certificacoes',
        # Cargo atual
        'cargo_atual_cargo_atual', 'cargo_atual_projeto_atual',
        'cargo_atual_cliente', 'cargo_atual_data_admissao',
        #Target
        'situacao_candidato'
    ]

    colunas_disponiveis = [col for col in colunas if col in df.columns]
    df = df[colunas_disponiveis].copy()

    if 'informacoes_pessoais_data_nascimento' in df:
        df['informacoes_pessoais_data_nascimento'] = pd.to_datetime(
            df['informacoes_pessoais_data_nascimento'], errors='coerce'
        )
        df['idade'] = df['informacoes_pessoais_data_nascimento'].apply(calcular_idade)
        df.drop(columns=['informacoes_pessoais_data_nascimento'], inplace=True)

    if 'cargo_atual_data_admissao' in df:
        df['cargo_atual_data_admissao'] = pd.to_datetime(
            df['cargo_atual_data_admissao'], errors='coerce'
        )
        df['tempo_empresa_anos'] = df['cargo_atual_data_admissao'].apply(
            lambda x: pd.Timestamp.now().year - x.year if pd.notnull(x) else np.nan
        )
        df.drop(columns=['cargo_atual_data_admissao'], inplace=True)

    vars_label = [
        'informacoes_pessoais_sexo', 'informacoes_pessoais_estado_civil',
        'informacoes_pessoais_pcd', 'infos_basicas_local',
        'infos_basicas_sabendo_de_nos_por', 'informacoes_pessoais_fonte_indicacao',
        'formacao_e_idiomas_nivel_academico', 'formacao_e_idiomas_nivel_ingles',
        'formacao_e_idiomas_nivel_espanhol', 'formacao_e_idiomas_outro_idioma',
        'formacao_e_idiomas_cursos', 'informacoes_profissionais_area_atuacao',
        'informacoes_profissionais_nivel_profissional',
        'informacoes_profissionais_certificacoes', 'cargo_atual_cargo_atual',
        'cargo_atual_projeto_atual', 'cargo_atual_cliente'
    ]
    for col in vars_label:
        if col in df:
            df[col] = df[col].astype(str)
            df[col] = LabelEncoder().fit_transform(df[col])

    return df

def salvar_dataset(df, path="data/processed/dataset_modelagem.parquet"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path)
    print(f"✅ Dataset salvo em: {path}")

def main():
    print("🔍 Carregando base geral...")
    df = carregar_base()

    print("⚙️ Selecionando e transformando variáveis...")
    df_tratado = selecionar_e_transformar(df)

    print("💾 Salvando dataset final para modelagem...")
    salvar_dataset(df_tratado)

if __name__ == "__main__":
    main()
