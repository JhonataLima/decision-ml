import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
from src.model.custom_transformers import label_encode_df

DATA_PATH = "data/processed/base_geral.parquet"

FEATURES = [
    'modalidade',
    'valor_venda',
    'titulo_vaga',
    'cliente',
    'requisitante',
    'analista_responsavel',
    'infos_basicas_objetivo_profissional',
    'infos_basicas_local',
    'infos_basicas_sabendo_de_nos_por',
    'informacoes_pessoais_data_nascimento',
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
    'cargo_atual_data_admissao'
]

TARGET = 'situacao_candidato'


def carregar_dados(path=DATA_PATH):
    df = pd.read_parquet(path)
    df = df.drop_duplicates()
    df = df.dropna(subset=[TARGET])
    return df


def transformar_dados(df):
    df = df.copy()

    df['informacoes_pessoais_data_nascimento'] = pd.to_datetime(
        df['informacoes_pessoais_data_nascimento'], errors='coerce'
    )
    df['cargo_atual_data_admissao'] = pd.to_datetime(
        df['cargo_atual_data_admissao'], errors='coerce'
    )

    df['idade'] = (
        pd.Timestamp.now().year - df['informacoes_pessoais_data_nascimento'].dt.year
    )
    df['anos_na_empresa'] = (
        pd.Timestamp.now().year - df['cargo_atual_data_admissao'].dt.year
    )

    df = df.drop(columns=['informacoes_pessoais_data_nascimento', 'cargo_atual_data_admissao'])

    final_features = [f for f in FEATURES if f in df.columns]
    final_features += ['idade', 'anos_na_empresa']

    X = df[final_features]
    y = df[TARGET]

    return X, y


def preparar_pipeline(X):
    cat_cols = X.select_dtypes(include='object').columns.tolist()
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    transformer = ColumnTransformer([
        ('label', FunctionTransformer(label_encode_df), cat_cols),
        ('num', 'passthrough', num_cols)
    ])

    pipeline = Pipeline([
        ('transformer', transformer)
    ])

    return pipeline


def salvar_dados(X_train, X_test, y_train, y_test, pipeline):
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    joblib.dump((X_train, X_test, y_train, y_test), "data/processed/dados_treinamento.pkl")
    joblib.dump(pipeline, "models/pipeline_transformacao.pkl")

from features.feature_selection import *


def main():
    print("Carregando dados...")
    df = carregar_dados()

    print("Transformando dados...")
    X, y = transformar_dados(df)

    print("Preparando pipeline de transformação...")
    pipeline = preparar_pipeline(X)

    print("Executando transformação e separando treino/teste...")
    X_transformed = pipeline.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.3, random_state=42, stratify=y)

    print("Salvando dados e pipeline...")
    salvar_dados(X_train, X_test, y_train, y_test, pipeline)

    print("✅ Feature selection e transformação finalizadas com sucesso.")


if __name__ == "__main__":
    main()