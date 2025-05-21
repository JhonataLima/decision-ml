import pandas as pd
import numpy as np
from datetime import datetime
import os


def carregar_base_unificada(caminho: str) -> pd.DataFrame:
    """
    Carrega a base unificada.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    return pd.read_parquet(caminho)


def gerar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera novas features para a base.
    """
    # Feature temporal
    if 'data_candidatura' in df.columns:
        df['data_candidatura'] = pd.to_datetime(df['data_candidatura'], errors='coerce')
        df['dias_desde_candidatura'] = (datetime.now() - df['data_candidatura']).dt.days

    # Feature de texto: tamanho do objetivo profissional
    if 'infos_basicas_objetivo_profissional' in df.columns:
        df['objetivo_len'] = df['infos_basicas_objetivo_profissional'].fillna('').apply(len)

    # Feature: quantidade de certificações
    if 'informacoes_profissionais_certificacoes' in df.columns:
        df['qtd_certificacoes'] = df['informacoes_profissionais_certificacoes'].fillna('').apply(lambda x: len(str(x).split(',')))

    # Feature booleana: possui LinkedIn
    if 'informacoes_pessoais_url_linkedin' in df.columns:
        df['possui_linkedin'] = df['informacoes_pessoais_url_linkedin'].notnull().astype(int)

    return df


def salvar_base(df: pd.DataFrame, caminho_saida: str):
    """
    Salva a base com novas features no formato Parquet.
    """
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_parquet(caminho_saida, index=False)
    print(f"Base enriquecida salva em: {caminho_saida}")


def main():
    caminho_entrada = "data/processed/base_geral.parquet"
    caminho_saida = "data/processed/feature_engineering.parquet"

    print("Carregando base unificada...")
    df = carregar_base_unificada(caminho_entrada)

    print("Gerando novas features...")
    df = gerar_features(df)

    print("Salvando base com novas features...")
    salvar_base(df, caminho_saida)

    print("Feature engineering finalizado com sucesso!")


if __name__ == "__main__":
    main()
