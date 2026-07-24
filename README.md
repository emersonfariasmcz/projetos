# 📊 Sales Data Pipeline & Advanced Analytical Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Viz-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

Projeto completo de **Engenharia de Dados e Analytics**, cobrindo desde o desenvolvimento de um pipeline modular de ETL (*Extract, Transform, Load*) até a análise exploratória avançada (EDA) com visualização executiva de KPIs de vendas, performance de canais e eficiência comercial.

---

## 📌 Sumário
- [Visão Geral do Projeto](#-visão-geral-do-projeto)
- [Arquitetura da Solução](#-arquitetura-da-solução)
- [Destaques Técnicos & Engenharia de Dados](#-destaques-técnicos--engenharia-de-dados)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Visualizações e Insights de Negócio](#-visualizações-e-insights-de-negócio)
- [Autor e Contato](#-autor-e-contato)

---

## 🎯 Visão Geral do Projeto

O objetivo deste projeto foi transformar dados brutos e desalinhados de vendas em um banco de dados relacional padronizado e otimizado para análises estratégicas.

A partir do banco relacional, foi desenvolvida uma suíte analítica com queries em SQL e visualizações interativas em Python, permitindo responder a perguntas cruciais de negócio:
- Qual é o faturamento bruto, líquido e o percentual médio de descontos?
- Quais canais de venda trazem maior volume financeiro e representatividade?
- Existe gargalo no ciclo de pagamento e histórico de inadimplência?
- Qual é a eficiência da força de vendas versus o custo de comissão pago por representante?

---

## 🏗️ Arquitetura da Solução

O fluxo da informação segue uma arquitetura moderna e reprodutível:

```text
+-----------------+       +-----------------------+       +----------------------+       +------------------------+
|  Dados Brutos   | ----> |  Pipeline de ETL      | ----> |  Database Relacional | ----> |  Análise Exploratória  |
|  (Excel / CSV)  |       |  (etl.py - Python)    |       |  (vendas.db - SQLite)|       |  (EDA_avancada.ipynb)  |
+-----------------+       +-----------------------+       +----------------------+       +------------------------+
```

1. **Ingestão & Limpeza (`etl.py`)**: Script modular com mapeamento dinâmico de colunas, normalização de strings para `snake_case` e padronização de datas para o formato ISO 8601 (`YYYY-MM-DD`).
2. **Armazenamento (`vendas.db`)**: Banco SQLite relacional otimizado para consultas analíticas rápidas.
3. **Analytics & Dashboards (`EDA_avancada.ipynb`)**: Notebook com consultas em SQL via Pandas, métricas executivas e gráficos interativos (Plotly e Seaborn).

---

## 🛠️ Destaques Técnicos & Engenharia de Dados

- **Mapeamento Tolerante a Falhas**: O script de ETL trata variações no cabeçalho das fontes brutas (ex: `Canal de Venda`, `canal_venda`, `canal`) garantindo resiliência na carga.
- **Padronização Automática**: Conversão dinâmica de nomes de colunas, tratamento de acentuação, caracteres especiais e preenchimento controlado de valores nulos (`NULL`).
- **Tratamento Temporal Avançado**: Normalização de datas e cálculos de variação temporal diretamente via funções nativas de SQL como `julianday()`.
- **Arquitetura Modular**: Separação clara entre a pipeline de ingestão de dados (`.py`) e a camada de visualização/análise (`.ipynb`).

---

## 📂 Estrutura do Repositório

```text
.
├── vendas.db              # Banco de dados relacional SQLite populado
├── etl.py                 # Pipeline modular de Extração, Transformação e Carga
├── EDA_avancada.ipynb     # Análise Exploratória e Dashboards Executivos
├── requirements.txt       # Dependências e bibliotecas Python do projeto
└── README.md              # Documentação oficial do repositório
```

---

## 🚀 Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Manipulação de Dados**: Pandas, NumPy
- **Banco de Dados**: SQLite3 (SQL)
- **Visualização de Dados**: Plotly Express, Seaborn, Matplotlib
- **Ambiente de Desenvolvimento**: VS Code & Google Colab

---

## 📈 Visualizações e Insights de Negócio

### 1. Métricas Executivas de Vendas (KPIs)
- **Total de Pedidos Processados**: 1.013
- **Faturamento Bruto Total**: R$ 3.184.771,00
- **Total de Descontos Concedidos**: R$ 236.223,67
- **Faturamento Líquido Final**: R$ 2.948.547,33
- **Ticket Médio**: R$ 2.910,71
- **Percentual Médio de Desconto**: 7,42%

### 2. Comparativo de Vendas por Canal
Análise do faturamento líquido acumulado por canal (Amazon, Mercado Livre, Magazine Luiza, Instagram, Facebook, Venda Direta e Americanas), identificando os canais de maior conversão financeira.

### 3. Relação entre Faturamento, Comissão e Volume por Vendedor
Gráfico de dispersão (*Scatter Plot*) correlacionando faturamento gerado, comissão total paga e volume de pedidos por vendedor, permitindo avaliar a eficiência comercial e custos operacionais.

---

## 👤 Autor e Contato

Desenvolvido por **Emerson Farias**.

- 💼 **LinkedIn**: [linkedin.com/in/emersonfarias](https://www.linkedin.com/in/emersonfarias) *(Atualize com seu link real)*
- 🐙 **GitHub**: [@emersonfariasmcz](https://github.com/emersonfariasmcz)

---
*Se este projeto ajudou você ou serviu de inspiração, não se esqueça de deixar uma ⭐️!*
