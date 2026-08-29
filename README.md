# Projeto de Análise de Gastos Públicos (Data Warehouse)

Este projeto implementa uma pipeline completa de **Data Warehouse (PostgreSQL)** para automação, limpeza, modelagem e análise de dados das despesas públicas federais.

O fluxo abrange desde a extração de dados brutos até a geração de inteligência de negócios por meio de **Jupyter Notebook**, consultas SQL, visualizações e pareceres explicativos.

---

## 📁 Estrutura do Projeto

```text
Projeto_Gastos_Publicos/
│
├── base-dados/
│   └── 202608_Despesas.csv         # Arquivo CSV bruto extraído
│
├── graficos/                       # Diretório para exportação dos gráficos gerados
│
├── servico/
│   ├── __pycache__/                # Cache de execução do Python
│   ├── scapper.py                  # Script de extração/download dos dados brutos
│   └── transformador.py            # Script de ETL, modelagem relacional e carga no DW
│
├── .env                            # Variáveis de ambiente e credenciais (ignorado pelo Git)
├── .gitignore                      # Arquivo de exclusão do Git
├── analise_despesas.ipynb          # Notebook com consultas SQL, gráficos e pareceres de negócio
├── execucao_etl.log                # Arquivo de log da execução do pipeline
├── main.py                         # Orquestrador principal da pipeline ETL
├── README.md                       # Documentação completa do projeto
└── requirements.txt                # Lista de dependências do projeto
```

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Banco de Dados:** PostgreSQL
* **Manipulação de Dados:** Pandas
* **Conexão com Banco:** SQLAlchemy e Psycopg2
* **Gerenciamento de Segredos:** python-dotenv
* **Visualização de Dados:** Matplotlib e Seaborn
* **Ambiente de Desenvolvimento:** VS Code e Jupyter Notebook

---

## ⚙️ Como Executar o Projeto

### 1. Instalar as Dependências

No terminal, execute:

```bash
pip install -r requirements.txt
```

### 2. Configurar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto e informe as credenciais de acesso ao PostgreSQL local:

```env
DB_USER=postgres
DB_PASSWORD=SuaSenhaAqui
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=dw_gastos_publicos
```

> **Importante:** o arquivo `.env` não deve ser versionado no Git, pois contém informações sensíveis de acesso ao banco de dados.

### 3. Executar a Pipeline ETL

Execute o script principal:

```bash
python main.py
```

A pipeline será responsável pelas etapas de:

1. Extração dos dados;
2. Tratamento e transformação;
3. Modelagem dos dados;
4. Carga no Data Warehouse;
5. Registro da execução no arquivo de log.

### 4. Executar as Análises de Negócio

Abra o arquivo:

```text
analise_despesas.ipynb
```

no VS Code ou Jupyter Notebook.

Execute as células para realizar as consultas SQL, gerar os gráficos na pasta `graficos/` e produzir os pareceres explicativos.

---

## 📘 Documentação do Projeto

### 🔄 Fluxo — Como o Projeto Funciona

#### 1. Extração

**Arquivo:** `servico/scapper.py`

Realiza a leitura e/ou extração dos dados orçamentários brutos utilizados pelo projeto, disponibilizando-os no diretório `base-dados/`.

#### 2. Transformação e Carga

**Arquivo:** `servico/transformador.py`

Responsável pelo processo de ETL, incluindo:

* Tratamento de valores nulos;
* Padronização e tipagem dos dados;
* Transformação das informações;
* Construção da modelagem dimensional;
* Implementação do **modelo Estrela (Star Schema)**;
* Carga dos dados no PostgreSQL.

#### 3. Análise e Visualização

**Arquivo:** `analise_despesas.ipynb`

Realiza consultas SQL diretamente no Data Warehouse, utilizando a **Tabela Fato** e as **Tabelas Dimensão** para gerar análises e indicadores.

Os gráficos gerados são armazenados no diretório:

```text
graficos/
```

#### 4. Monitoramento e Segurança

O módulo `logging` registra os eventos de execução da pipeline no arquivo:

```text
execucao_etl.log
```

As credenciais de acesso ao PostgreSQL são armazenadas no arquivo `.env`, protegido pelo `.gitignore`.

---

## 📊 Schemas de Dados

O Data Warehouse é estruturado utilizando **modelo dimensional (Star Schema)**, composto por **1 Tabela Fato e 4 Tabelas Dimensão**.

| Tabela                 | Tipo     | Campos Principais                                                                                                 | Descrição                                                              |
| ---------------------- | -------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `fato_despesas`        | Fato     | `id_fato`, `id_orgao`, `id_funcao`, `id_elemento`, `id_tempo`, `valor_empenhado`, `valor_liquidado`, `valor_pago` | Contém as métricas financeiras e as chaves estrangeiras das dimensões. |
| `dim_orgao`            | Dimensão | `id_orgao`, `nome_orgao_superior`, `nome_orgao_subordinado`                                                       | Contém a estrutura hierárquica dos órgãos.                             |
| `dim_funcao`           | Dimensão | `id_funcao`, `nome_funcao`, `nome_subfuncao`                                                                      | Mapeia as funções orçamentárias do governo.                            |
| `dim_elemento_despesa` | Dimensão | `id_elemento`, `nome_grupo`, `nome_elemento`                                                                      | Classifica a natureza técnica da despesa.                              |
| `dim_tempo`            | Dimensão | `id_tempo`, `data`, `ano`, `mes`, `dia`                                                                           | Registra a dimensão temporal dos gastos.                               |

### ⭐ Modelo Dimensional

A `fato_despesas` concentra as principais métricas financeiras e se relaciona com as dimensões responsáveis por fornecer os diferentes contextos de análise:

```text
                    dim_orgao
                       │
                       │
dim_funcao ───── fato_despesas ───── dim_elemento_despesa
                       │
                       │
                   dim_tempo
```

Esse modelo facilita a realização de consultas analíticas, agregações e cruzamentos entre diferentes perspectivas dos gastos públicos.

---

## 💡 Respostas para as Perguntas do Projeto

### 1. Ranking dos 5 Órgãos Superiores com Maiores Gastos Liquidados

**Raciocínio de Negócio:**

Mapear onde se concentra o maior volume de recursos públicos liquidados para orientar auditorias e o acompanhamento da execução orçamentária.

**Parecer Técnico:**

A maior parte dos desembolsos está concentrada em ministérios responsáveis por transferências constitucionais, previdência e saúde. Devido ao alto volume financeiro envolvido, otimizações operacionais nessas pastas podem gerar impacto orçamentário relevante.

---

### 2. Gastos Totais por Área/Função de Governo

**Raciocínio de Negócio:**

Identificar quais áreas temáticas recebem as maiores parcelas do orçamento federal e monitorar a efetividade da execução dos pagamentos.

**Parecer Técnico:**

As funções de **Encargos Especiais, Previdência Social e Saúde** concentram os maiores totais pagos. Eventuais discrepâncias entre empenho e pagamento nessas áreas podem indicar pontos de atenção na execução orçamentária.

---

### 3. Comparativo da Execução Orçamentária

**Empenhado × Liquidado × Pago**

**Raciocínio de Negócio:**

Medir o nível de execução das obrigações assumidas pelo Governo Federal e identificar diferenças entre as etapas da despesa pública.

**Parecer Técnico:**

Despesas correntes, como pessoal, apresentam alta conversão de empenho em pagamento. Em contrapartida, despesas de capital, como investimentos, podem apresentar diferenças entre os valores empenhados e liquidados, refletindo a complexidade dos prazos envolvidos em obras, contratos e processos de licitação.

---

## 🔮 Possíveis Melhorias Futuras

### Orquestração de Pipelines

Implementação de ferramentas como **Apache Airflow** ou **Prefect** para permitir o agendamento e monitoramento automático das rotinas de ETL.

### Data Quality

Aplicação de frameworks de validação, como **Great Expectations**, para verificar regras de integridade, consistência e qualidade dos dados durante o processo de ETL.

### Dashboards Interativos

Conexão do Data Warehouse com ferramentas de Business Intelligence, como **Power BI** ou **Looker Studio**, para criação de dashboards e visões analíticas interativas.

---

## ✍️ Autoria e Identificação

**Aluna:** Caroline de Souza Cunha Lopes

**Programa:** Carreira Tech — SENAI/SCTEC

**Módulo:** Módulo 2 — Arquitetura e Modelagem de Dados

**Turma:** T1
