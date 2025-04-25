
# 📄 Documentação dos Arquivos JSON

## 1. `vagas.json`

### ✅ Descrição
Contém as informações completas sobre as vagas abertas, incluindo dados administrativos, perfil técnico desejado e benefícios.

### 🧱 Estrutura
```json
{
  "id_vaga": {
    "informacoes_basicas": { ... },
    "perfil_vaga": { ... },
    "beneficios": { ... }
  }
}
```

### 📌 Campos principais

#### `informacoes_basicas`
- `data_requicisao`: Data da requisição da vaga  
- `titulo_vaga`: Título da vaga  
- `cliente`: Nome do cliente  
- `tipo_contratacao`: Tipo de contrato (CLT, PJ, etc.)  
- `analista_responsavel`, `requisitante`, `solicitante_cliente`: Pessoas envolvidas  

#### `perfil_vaga`
- `pais`, `estado`, `cidade`: Local da vaga  
- `nivel_profissional`, `nivel_academico`: Nível esperado  
- `nivel_ingles`, `nivel_espanhol`, `outro_idioma`: Requisitos de idioma  
- `principais_atividades`: Texto com responsabilidades  
- `competencia_tecnicas_e_comportamentais`: Requisitos técnicos e soft skills  
- `demais_observacoes`, `viagens_requeridas`, `equipamentos_necessarios`  

#### `beneficios`
- `valor_venda`, `valor_compra_1`, `valor_compra_2`: Informações financeiras da vaga  

---

## 2. `prospects.json`

### ✅ Descrição
Lista os profissionais prospectados para cada vaga, incluindo status no processo seletivo e comentários de recrutadores.

### 🧱 Estrutura
```json
{
  "id_vaga": {
    "prospects": [
      {
        "codigo": "id_profissional",
        "nome": "Nome do prospect",
        "situacao": "Status (ex: Contratado, Rejeitado)",
        "data": "Data do evento",
        "comentario": "Feedback do recrutador",
        ...
      }
    ]
  }
}
```

### 📌 Campos principais por prospect
- `codigo`: Identificador único do candidato, relacionável com `applicants.json`  
- `nome`: Nome do candidato  
- `situacao`: Situação no processo (ex: Em andamento, Rejeitado, Contratado)  
- `data`: Data do registro  
- `comentario`: Observações e avaliações feitas por recrutadores  
- `recrutador`, `responsavel`, `codigo_profissional`, etc.  

---

## 3. `applicants.json`

### ✅ Descrição
Informações detalhadas dos profissionais cadastrados, incluindo dados pessoais, formação, experiência e currículos em texto.

### 🧱 Estrutura
```json
{
  "codigo_profissional": {
    "dados": {
      "nome", "email", "telefone", ...
    },
    "formacoes": [ ... ],
    "idiomas": [ ... ],
    "experiencias_profissionais": [ ... ],
    "cv_texto_pt": "...",
    "cv_texto_en": "..."
  }
}
```

### 📌 Campos principais

#### `dados`
- Informações pessoais e básicas do profissional  
- `nivel_profissional`, `nivel_academico`, `nivel_ingles`, etc.  

#### `formacoes`
- Lista de cursos, instituição, status e nível acadêmico  

#### `idiomas`
- Idiomas e níveis de fluência  

#### `experiencias_profissionais`
- Histórico de empresas, cargos e atividades  

#### `cv_texto_pt`, `cv_texto_en`
- Currículo em texto livre, útil para NLP  

---

## 🔗 Relacionamentos entre arquivos

| Fonte        | Campo Relacional             | Relacionamento com |
|--------------|-------------------------------|---------------------|
| `prospects`  | `id_vaga`                    | `vagas`             |
| `prospects`  | `codigo` / `codigo_profissional` | `applicants`        |

---

## 🎯 Aplicações esperadas
Com esses dados, é possível construir:
- Sistema de **recomendação de candidatos por vaga**
- Modelo de **match preditivo** baseado no histórico
- **Análise textual** de currículos e comentários
- Painel de **perfilamento de candidatos e vagas**
