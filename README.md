# 📈 Fintech Data Pipeline & Financial Analytics

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-11557c?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)

Aplicação desenvolvida para processamento, limpeza, engenharia de dados e análise exploratória de logs transacionais brutos de uma Fintech. O pipeline trata encoders legados, realiza enriquecimento temporal com timezone específico, detecta anomalias estatísticas via Z-Score e gera relatórios visuais de desempenho.

---

## 🚀 Funcionalidades do Pipeline

1. **Ingestão e Limpeza:**
   - Leitura de logs com suporte a encoding legado (`latin1`).
   - Imputação de valores nulos (`NaN`) na coluna `valor` utilizando a **mediana regional por estado**.
   - Adição de coluna estática para rastreabilidade de plataforma.

2. **Engenharia de Dados e Ajuste Temporal:**
   - Conversão de datas para `datetime64[ns]` com suporte ao fuso horário local (`America/Sao_Paulo`).
   - Extração do dia da semana e mês da transação.
   - Remoção de registros duplicados mantendo a primeira ocorrência.

3. **Filtragem Vetorizada:**
   - Consultas otimizadas com operadores bitwise (`&`, `|`) para filtragem de transações de alto valor em estados específicos.

4. **Cruzamento de Dados e Agregação:**
   - Mapeamento dinâmico de risco por cliente (`.map()`).
   - Construção de Tabela Dinâmica (`pivot_table`) com subtotais agregados por risco e mês.

5. **Detecção Estatística de Anomalias (Z-Score):**
   - Cálculo vetorizado sem laços `for` do Z-Score relativo ao grupo do estado:
     $$Z = \frac{x - \mu}{\sigma}$$
   - Identificação automatizada de potenciais fraudes/outliers ($Z > 2.5$).

6. **Relatórios Visuais (API Orientada a Objetos):**
   - Gráfico de linhas comparando o volume diário com a **Média Móvel de 7 dias**.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Pandas**: Manipulação e agregação de dados.
- **NumPy**: Operações vetorizadas e cálculo estatístico.
- **Matplotlib**: Visualização de dados com API Orientada a Objetos.

---

## 📂 Estrutura do Repositório

```text
.
├── criar_dados.py          # Script auxiliar para geração de logs brutos (CSV)
├── pipeline.py             # Script principal de ETL e Análise de Dados
├── requirements.txt        # Dependências do projeto
├── relatorio_transacoes.png# Gráfico exportado pelo pipeline
└── README.md               # Documentação do projeto