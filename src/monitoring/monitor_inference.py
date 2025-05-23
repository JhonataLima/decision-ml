import os
import pandas as pd
import datetime
import json

LOG_FILE = "logs/logs_inferencia.csv"
os.makedirs("logs", exist_ok=True)


def inicializar_log():
    if not os.path.exists(LOG_FILE):
        df_vazio = pd.DataFrame(columns=[
            "timestamp", "input_data", "prediction"
        ])
        df_vazio.to_csv(LOG_FILE, index=False)


def registrar_inferencia(input_data, prediction):
    """Salva a entrada e saída do modelo com timestamp"""
    timestamp = datetime.datetime.now().isoformat()
    
    registro = {
        "timestamp": timestamp,
        "input_data": json.dumps(input_data, ensure_ascii=False),
        "prediction": prediction
    }

    df = pd.DataFrame([registro])
    df.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)


def mostrar_estatisticas():
    """Mostra estatísticas básicas de inferência"""
    if not os.path.exists(LOG_FILE):
        print("Nenhum log encontrado.")
        return

    df = pd.read_csv(LOG_FILE)
    print("\n📊 Estatísticas de Inferência:")
    print(f"Total de requisições: {len(df)}")
    print("Últimos 5 registros:")
    print(df.tail())


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o log se não existir
    inicializar_log()

    # Simulação de inferências
    exemplo_input = {
        "informacoes_pessoais_nome": "João",
        "informacoes_profissionais_area_atuacao": "TI",
        "informacoes_profissionais_nivel_profissional": "Pleno"
    }

    predicao_exemplo = "match"

    # Registrar a inferência
    registrar_inferencia(exemplo_input, predicao_exemplo)

    # Ver estatísticas
    mostrar_estatisticas()
