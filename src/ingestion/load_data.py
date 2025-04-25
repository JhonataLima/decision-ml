import json
import os
import pandas as pd
from pathlib import Path

CAMINHO_DADOS_BRUTOS = Path("data/raw")
CAMINHO_SAIDA = Path("data/processed/base_geral.parquet")


def carregar_json(caminho):
    """
    Carrega um arquivo JSON a partir do caminho especificado.

    Parâmetros:
        caminho (str | Path): Caminho para o arquivo JSON.

    Retorna:
        dict: Dados carregados em formato de dicionário.
    """
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_todos_os_dados():
    """
    Carrega todos os arquivos JSON necessários para o projeto.

    Retorna:
        tuple: Contendo os dados de vagas, prospects e candidatos.
    """
    vagas = carregar_json(CAMINHO_DADOS_BRUTOS / "vagas.json")
    prospects = carregar_json(CAMINHO_DADOS_BRUTOS / "prospects.json")
    candidatos = carregar_json(CAMINHO_DADOS_BRUTOS / "applicants.json")
    return vagas, prospects, candidatos


def achatar_dados(vagas, prospects, candidatos):
    """
    Realiza o merge entre vagas, prospects e candidatos, consolidando
    os dados em um único DataFrame.

    Parâmetros:
        vagas (dict): Dicionário com dados das vagas.
        prospects (dict): Dicionário com os candidatos prospectados por vaga.
        candidatos (dict): Dicionário com dados completos dos candidatos.

    Retorna:
        pd.DataFrame: DataFrame consolidado com todas as informações.
    """
    registros = []

    for vaga_id, vaga in vagas.items():
        info_basica = vaga.get("informacoes_basicas", {})
        perfil = vaga.get("perfil_vaga", {})
        beneficios = vaga.get("beneficios", {})

        lista_prospects = prospects.get(vaga_id, {}).get("prospects", [])

        for prospect in lista_prospects:
            candidato_id = str(prospect.get("codigo", ""))
            registro = {
                "vaga_id": vaga_id,
                "titulo_vaga": info_basica.get("titulo_vaga", ""),
                "cliente": info_basica.get("cliente", ""),
                "requisitante": info_basica.get("requisitante", ""),
                "analista_responsavel": info_basica.get("analista_responsavel", ""),
                "modalidade": perfil.get("modalidade", ""),
                "valor_venda": beneficios.get("valor_venda", ""),
                "nome_prospect": prospect.get("nome", ""),
                "codigo_prospect": candidato_id,
                "situacao_candidato": prospect.get("situacao_candidato", ""),
                "data_candidatura": prospect.get("data_candidatura", ""),
                "ultima_atualizacao": prospect.get("ultima_atualizacao", ""),
                "comentario": prospect.get("comentario", ""),
                "recrutador": prospect.get("recrutador", "")
            }

            if candidato_id in candidatos:
                dados_candidato = candidatos[candidato_id]
                for chave, valor in dados_candidato.items():
                    if isinstance(valor, dict):
                        for sub_chave, sub_valor in valor.items():
                            registro[f"{chave}_{sub_chave}"] = sub_valor
                    else:
                        registro[chave] = valor

            registros.append(registro)

    df = pd.DataFrame(registros)
    return df


def salvar_dataframe(df):
    """
    Salva o DataFrame consolidado em formato Parquet.

    Parâmetros:
        df (pd.DataFrame): DataFrame a ser salvo.
    """
    os.makedirs(CAMINHO_SAIDA.parent, exist_ok=True)
    df.to_parquet(CAMINHO_SAIDA, index=False)
    print(f"✅ Base consolidada salva em: {CAMINHO_SAIDA}")


def main():
    print("📥 Carregando arquivos JSON...")
    vagas, prospects, candidatos = carregar_todos_os_dados()

    print("🔄 Consolidando dados...")
    df_consolidado = achatar_dados(vagas, prospects, candidatos)

    print("💾 Salvando base processada...")
    salvar_dataframe(df_consolidado)


if __name__ == "__main__":
    main()
    print("🚀 Script executado com sucesso!")