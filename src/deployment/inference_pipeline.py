import joblib
import pandas as pd
import os
import traceback

PIPELINE_PATH = "models/pipeline_transformacao.pkl"
MODEL_PATH = "models/random_forest_model.pkl"

def carregar_pipeline():
    return joblib.load(PIPELINE_PATH)

def carregar_modelo():
    return joblib.load(MODEL_PATH)

def carregar_novos_dados(path_csv):
    try:
        df = pd.read_csv(path_csv)
        print(f"✅ Dados carregados de {path_csv} com {df.shape[0]} linhas.")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        raise

def tratar_dados_brutos(dados, colunas_esperadas):
    dados = dados.copy()
    
    for col in colunas_esperadas:
        if col not in dados.columns:
            dados[col] = None
    
    dados = dados[colunas_esperadas]
    
    dados = dados.fillna("")
    
    return dados

def fazer_predicao(dados, pipeline, modelo):
    try:
        colunas_esperadas = pipeline.feature_names_in_
        dados_tratados = tratar_dados_brutos(dados, colunas_esperadas)
        dados_transformados = pipeline.transform(dados_tratados)
        predicoes = modelo.predict(dados_transformados)
        return predicoes
    except Exception as e:
        print("❌ Erro ao fazer predição:")
        traceback.print_exc()
        raise

def salvar_resultado(dados, predicoes, path_saida):
    dados['predicao'] = predicoes
    dados.to_csv(path_saida, index=False)
    print(f"✅ Resultado salvo em: {path_saida}")

def main():
    try:
        dados = carregar_novos_dados("data/inference/dados_testes.csv")
        pipeline = carregar_pipeline()
        modelo = carregar_modelo()

        predicoes = fazer_predicao(dados, pipeline, modelo)
        salvar_resultado(dados, predicoes, "data/inference/resultado_inferencias.csv")

        print("✅ Inferência concluída com sucesso!")
    except Exception as e:
        print("❌ Falha na inferência.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
