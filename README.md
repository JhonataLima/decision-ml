```bash
decision-ml/
├── data/
│   ├── raw/                 # Dados brutos: applicants.json, prospects.json, vagas.json
│   ├── processed/           # Dados tratados/formatados
│   └── README.md            # Instruções sobre a origem e processamento dos dados
│
├── docs/
│   ├── data_sources/        # Documentação sobre as fontes de dados (jsons, APIs, etc.)
│   │   └── documentacao_jsons_decision.md
│   ├── architecture.md      # Documentação da arquitetura do projeto
│   ├── model_deployment.md  # Como o modelo será implementado e disponibilizado
│   └── README.md            # Visão geral do projeto, arquitetura, dependências
│
├── notebooks/               # Notebooks de exploração e experimentação
│   ├── exploratory/         # Notebooks exploratórios e análise de dados
│   └── model_building/      # Notebooks de desenvolvimento e treinamento de modelos
│
├── src/                     # Código-fonte do pipeline de ML
│   ├── ingestion/           # Ingestão e parse dos dados JSON
│   ├── preprocessing/       # Pré-processamento e transformação dos dados
│   ├── models/              # Implementação dos modelos (match, clusterização, etc.)
│   ├── evaluation/          # Avaliação e validação dos modelos
│   └── deployment/          # Scripts para deploy de modelos (APIs, containers, etc.)
│
├── tests/                   # Testes unitários e de integração
│   ├── test_preprocessing.py # Testes sobre as transformações de dados
│   ├── test_models.py       # Testes sobre os modelos de ML
│   └── test_deployment.py   # Testes sobre o deploy e integração
│
├── requirements.txt         # Dependências do projeto
├── environment.yml          # Ambiente Conda (se necessário)
├── README.md                # Visão geral do projeto, como rodar e contribuir
└── .gitignore               # Arquivos e pastas ignorados no git
```