# Netflix Shows Analytics
> Análise exploratória e visualização interativa do catálogo da Netflix (filmes e séries).

## 📋 Tema do Projeto

Analisar o conjunto de dados "Netflix Shows" (Kaggle) para entender a composição do catálogo, identificar tendências de lançamentos, gêneros mais populares, distribuição geográfica e outras métricas relevantes, apresentando tudo em um dashboard interativo.

## 👥 Integrantes

| Nome      | GitHub               | Responsabilidade                     |
|-----------|----------------------|--------------------------------------|
| Rubia     | @rubia-github        | Definição da base de dados           |
| Nicolas   | @nicolas-github      | Estruturação do repositório e README |
| Felipe    | @felipe-github       | Transformações (limpeza, tipos)      |
| Vanderson | @vanderson-github    | Protótipo do Dashboard               |
| Isaac     | @isaac-github        | Implementação do ETL com Pandas      |

## 🎯 Objetivo da Análise

- Explorar a diversidade de gêneros, países e durações presentes no catálogo.
- Identificar tendências temporais de adição de títulos.
- Disponibilizar um dashboard que permita ao usuário filtrar e comparar métricas de forma dinâmica.

## 📂 Estrutura do Repositório

```
netflix-shows-analytics/
│
├─ data/
│  ├─ raw/          # CSV original (não versionado)
│  └─ processed/    # Dados limpos (Parquet/CSV)
│
├─ notebooks/
│  └─ 01-exploracao.ipynb
│
├─ src/
│  ├─ __init__.py
│  ├─ etl.py
│  └─ utils.py
│
├─ dashboard/
│  └─ app.py
│
├─ docs/
│  └─ .gitkeep
│
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## 📅 Planejamento

### Primeira Etapa — Planejamento e Estruturação (entrega: 23/03)

| Data  | Marco                                            | Responsável    |
|-------|--------------------------------------------------|----------------|
| 10/02 | Criação do repositório + adicionar colaboradores | Nicolas        |
| 17/02 | Download e versionamento do CSV                  | Rubia          |
| 24/02 | Definição e descrição da base de dados no README | Rubia          |
| 03/03 | Definição das tarefas de cada integrante         | Todos          |
| 10/03 | Esboço das transformações planejadas             | Felipe & Isaac |
| 14/03 | Wireframe e ideia inicial do dashboard           | Vanderson      |
| 19/03 | Cronograma de desenvolvimento no README          | Nicolas        |
| 22/03 | Revisão geral do README                          | Todos          |
| 23/03 | ✅ Entrega da Primeira Etapa                     | Todos          |

### Segunda Etapa — ETL e Dashboard (entrega: 27/07)

| Data  | Marco                                                  | Responsável        |
|-------|--------------------------------------------------------|--------------------|
| 07/04 | Extração e validação do CSV bruto                      | Rubia              |
| 14/04 | Notebook exploratório (`01-exploracao.ipynb`)          | Felipe & Isaac     |
| 05/05 | Limpeza e padronização dos dados (nulos, tipos)        | Felipe             |
| 12/05 | Colunas derivadas (`duration_value`, `duration_unit`)  | Felipe             |
| 19/05 | Tabelas auxiliares (`genres.parquet`, `countries.parquet`) | Isaac          |
| 26/05 | Script ETL completo em `src/etl.py`                    | Isaac              |
| 02/06 | Armazenamento dos dados tratados em `data/processed/`  | Isaac              |
| 09/06 | Estrutura base do dashboard (`dashboard/app.py`)       | Vanderson          |
| 16/06 | Implementação dos 6 gráficos + sidebar de filtros      | Vanderson          |
| 23/06 | Testes de integração ETL ↔ Dashboard                   | Isaac & Vanderson  |
| 07/07 | Publicação do dashboard (Streamlit Cloud)              | Vanderson          |
| 14/07 | Testes finais e ajustes                                | Todos              |
| 21/07 | Revisão do README e documentação final                 | Nicolas            |
| 27/07 | ✅ Entrega Final da Segunda Etapa                      | Todos              |

## 🔧 Transformações Planejadas

- Conversão de `date_added` → `datetime`.
- Explosão das colunas `cast` e `listed_in` em tabelas auxiliares.
- Tratamento de valores nulos (`Desconhecido` ou remoção de linhas).
- Criação de colunas derivadas (`duration_value`, `duration_unit`).
- Geração de datasets intermediários (`genres.parquet`, `countries.parquet`).

## 📊 Ideia Inicial do Dashboard

- **Sidebar** com filtros: Ano de lançamento, Gênero, País, Tipo (Movie/TV Show).
- **Gráficos principais**:
  1. Bar – Quantidade por tipo.
  2. Bar – Top 10 gêneros.
  3. Line – Lançamentos ao longo dos anos.
  4. Pie – Distribuição de ratings.
  5. Map (choropleth) – Conteúdo por país.
  6. Box/Violin – Duração média por gênero.

> O dashboard será desenvolvido em **Streamlit** (arquivo `dashboard/app.py`).  
> Dependências: `pandas`, `numpy`, `streamlit`, `plotly`, `pydeck`.

## 📚 Referências

- [Kaggle – Netflix Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- [Pandas docs](https://pandas.pydata.org/docs/)
- [Streamlit docs](https://docs.streamlit.io/)
