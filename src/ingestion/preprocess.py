import pandas as pd

# Colunas por tipo
dados_colunas_string = [
    'vaga_id', 'titulo_vaga', 'cliente', 'requisitante', 'analista_responsavel', 'modalidade',
    'nome_prospect', 'codigo_prospect', 'situacao_candidato', 'comentario', 'recrutador',
    'infos_basicas_telefone_recado', 'infos_basicas_telefone', 'infos_basicas_objetivo_profissional',
    'infos_basicas_inserido_por', 'infos_basicas_email', 'infos_basicas_local', 'infos_basicas_sabendo_de_nos_por',
    'infos_basicas_codigo_profissional', 'infos_basicas_nome',
    'informacoes_pessoais_nome', 'informacoes_pessoais_cpf', 'informacoes_pessoais_fonte_indicacao',
    'informacoes_pessoais_email', 'informacoes_pessoais_email_secundario', 'informacoes_pessoais_telefone_celular',
    'informacoes_pessoais_telefone_recado', 'informacoes_pessoais_sexo', 'informacoes_pessoais_estado_civil',
    'informacoes_pessoais_pcd', 'informacoes_pessoais_endereco', 'informacoes_pessoais_skype',
    'informacoes_pessoais_url_linkedin', 'informacoes_pessoais_facebook',
    'informacoes_profissionais_titulo_profissional', 'informacoes_profissionais_area_atuacao',
    'informacoes_profissionais_conhecimentos_tecnicos', 'informacoes_profissionais_certificacoes',
    'informacoes_profissionais_outras_certificacoes', 'informacoes_profissionais_nivel_profissional',
    'formacao_e_idiomas_nivel_academico', 'formacao_e_idiomas_nivel_ingles',
    'formacao_e_idiomas_nivel_espanhol', 'formacao_e_idiomas_outro_idioma',
    'cv_pt', 'cv_en', 'formacao_e_idiomas_instituicao_ensino_superior',
    'formacao_e_idiomas_cursos', 'formacao_e_idiomas_outro_curso',
    'informacoes_profissionais_qualificacoes', 'informacoes_profissionais_experiencias',
    'cargo_atual_id_ibrati', 'cargo_atual_email_corporativo', 'cargo_atual_cargo_atual',
    'cargo_atual_projeto_atual', 'cargo_atual_cliente', 'cargo_atual_unidade',
    'cargo_atual_nome_superior_imediato', 'cargo_atual_email_superior_imediato',
    'informacoes_pessoais_data_aceite'
]

dados_colunas_numericas = [
    'valor_venda', 'informacoes_profissionais_remuneracao', 'formacao_e_idiomas_ano_conclusao'
]

dados_colunas_datas = [
    'data_candidatura', 'ultima_atualizacao', 'infos_basicas_data_criacao',
    'infos_basicas_data_atualizacao',
    'informacoes_pessoais_data_nascimento', 'cargo_atual_data_admissao',
    'cargo_atual_data_ultima_promocao'
]

def carregar_base_geral():
    caminho = "data/processed/base_geral.parquet"
    return pd.read_parquet(caminho)

def ajustar_tipos(df):
    for col in dados_colunas_string:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in dados_colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in dados_colunas_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def limpar_transformar_base(df):
    df = df.drop_duplicates()
    df = ajustar_tipos(df)
    return df

def salvar_dados(df):
    df.to_parquet("data/processed/base_tratada.parquet")
    print("✅ Base tratada salva com sucesso!")

def main():
    df = carregar_base_geral()
    df = limpar_transformar_base(df)
    salvar_dados(df)

if __name__ == "__main__":
    main()