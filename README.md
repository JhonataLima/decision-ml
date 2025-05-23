
# 🔍 Decision ML - Projeto de Machine Learning Engineering

Este repositório contém uma solução completa de Engenharia de Machine Learning aplicada ao case da empresa **Decision**, incluindo pré-processamento, modelagem, deploy com API e monitoramento de inferências.

---

## 📁 Estrutura do Projeto

```
decision-ml/
├── data/                 # Dados brutos e processados
├── logs/                 # Logs de inferências
├── models/               # Modelos e pipelines salvos
├── notebooks/            # Análises exploratórias (EDA)
├── src/
│   ├── ingestion/        # Leitura e unificação dos dados
│   ├── model/            # Treinamento do modelo
│   ├── deployment/       # Inferência e API (FastAPI)
│   ├── evaluation/       # Avaliação do modelo
│   └── monitoring/       # Registro de inferências
├── Dockerfile            # Empacotamento da API
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto
```

---

## 🚀 Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/decision-ml.git
cd decision-ml
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
Baixe os [arquivos](https://drive.google.com/drive/folders/1f3jtTRyOK-PBvND3JTPTAxHpnSrH7rFR) para a pasta data/raw ante de inciar a execução.

### 4. Execute o pipeline de treinamento
```bash
python src/model/train_model_pipeline.py
```

---

## 🧠 Como rodar a API (FastAPI)

```bash
uvicorn src.deployment.predict:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Como usar com Docker

### 1. Build da imagem Docker
```bash
docker build -t decision-ml-api .
```

### 2. Rodar o container
```bash
docker run -p 8000:8000 decision-ml-api
```

Acesse a API em [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📝 Como fazer uma previsão

Você pode usar o [Postman](https://www.postman.com/) ou cURL:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"campo1": "valor", "campo2": 123, ...}'
```

---

## 📊 Monitoramento de inferência

Toda requisição feita à API é registrada no arquivo:

```bash
logs/logs_inferencia.csv
```

Inclui:
- Dados de entrada
- Previsão feita
- Timestamp

---

## ☁️ Deploy em nuvem

Você pode realizar deploy via:
- Google Cloud Run
- Render
- Heroku
- AWS Elastic Beanstalk

(O deploy local via Docker já garante replicabilidade.)

---

## 🎥 Entrega

1. Repositório completo no GitHub ✅  
2. Link da API via Docker ou nuvem ✅  
3. Vídeo com explicação do projeto ([até 5 min](https://youtu.be/izDjfj_WOas)) ✅  

---

## 👨‍💻 Autor

Projeto desenvolvido por Jhonata Lima, no contexto do Datathon de Machine Learning Engineering da FIAP.

---
