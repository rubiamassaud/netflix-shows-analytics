# Netflix Shows Analytics
> Análise exploratória e visualização interativa do catálogo da Netflix (filmes e séries).

## 📋 Tema do Projeto

Analisar o conjunto de dados ["Netflix Shows" (Kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows) para entender a composição do catálogo, identificar tendências de lançamentos, gêneros mais populares, distribuição geográfica e outras métricas relevantes, apresentando tudo em um dashboard interativo.

## 👥 Integrantes

| Nome      | GitHub               | Responsabilidade                     |
|-----------|----------------------|--------------------------------------|
| Rubia     | @rubiamassaud        | Definição da base de dados           |
| Nicolas   | @nicolasenne      | Estruturação do repositório e README |
| Felipe    | @FelipeBalikian      | Transformações (limpeza, tipos)      |
| Vanderson | @Vandersonlcm    | Protótipo do Dashboard               |
| Isaac     | @Isaac09122        | Implementação do ETL com Pandas      |

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
│  ├─ utils.py
│  └─ validate_raw.py
│
├─ dashboard/
│  └─ app.py
│
├─ docs/
│  ├─ .gitkeep
│  └─ validacao_raw.md
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

### Segunda Etapa — ETL e Dashboard (entrega: 18/05)

| Data  | Marco                                                  | Responsável        |
|-------|--------------------------------------------------------|--------------------|
| 25/04 | Extração e validação do CSV bruto                      | Rubia              |
| 30/04 | Notebook exploratório (`01-exploracao.ipynb`)          | Felipe & Isaac     |
| 05/05 | Limpeza e padronização dos dados (nulos, tipos)        | Felipe             |
| 05/05 | Colunas derivadas (`duration_value`, `duration_unit`)  | Felipe             |
| 08/05 | Tabelas auxiliares (`genres.parquet`, `countries.parquet`) | Isaac          |
| 11/05 | Script ETL completo em `src/etl.py`                    | Isaac              |
| 11/05 | Armazenamento dos dados tratados em `data/processed/`  | Isaac              |
| 13/05 | Estrutura base do dashboard (`dashboard/app.py`)       | Vanderson          |
| 15/05 | Implementação dos 6 gráficos + sidebar de filtros      | Vanderson          |
| 16/05 | Testes de integração ETL ↔ Dashboard                   | Isaac & Vanderson  |
| 17/05 | Publicação do dashboard (Streamlit Cloud)              | Vanderson          |
| 17/05 | Testes finais e ajustes                                | Todos              |
| 17/05 | Revisão do README e documentação final                 | Nicolas            |
| 18/05 | ✅ Entrega Final da Segunda Etapa                      | Todos              |

## 🔧 Transformações Planejadas

### Limpeza e padronização
- Converter date_added de texto para datetime.
- Remover registros duplicados.
- Preencher nulos em country, director e cast com "Unknown" e rating com "Not Rated".
- Padronizar strings (remover espaços extras).
- Separar duration em duration_value (int) e duration_unit ("minutes" ou "seasons").
- Garantir que duration_value seja numérico.

### Colunas derivadas
- year_added e month_added extraídos de date_added.
- is_movie (booleano) indicando se o conteúdo é filme.
- Possível criação de title_length para análise exploratória.

### Tabelas auxiliares
- genres.parquet — explosão de listed_in (uma linha por gênero).
- countries.parquet — explosão de country (uma linha por país).

### Saída de dados
- netflix_clean.parquet — dataset principal limpo.
- genres.parquet — tabela de gêneros normalizados.
- countries.parquet — tabela de países normalizados.

## 📊 Ideia Inicial do Dashboard

- **Sidebar** com filtros: Ano de lançamento, Gênero, País, Tipo (Movie/TV Show).
- **Gráficos principais**:
  1. Bar – Quantidade por tipo.
  2. Bar – Top 10 gêneros.
  3. Line – Lançamentos ao longo dos anos.
  4. Pie – Distribuição de ratings.
  5. Bar – Top países com maior quantidade de títulos.
  6. Box/Violin – Duração média por gênero.

> O dashboard será desenvolvido em **Streamlit** (arquivo `dashboard/app.py`).  
> Dependências: `pandas`, `numpy`, `streamlit`, `plotly`, `pydeck`.

## ✅ Entregas implementadas na parte do Isaac

A parte de ETL foi implementada em `src/etl.py` com as seguintes funções:

- leitura do CSV bruto em `data/raw/netflix_titles.csv`;
- limpeza e padronização dos dados;
- remoção de duplicidades por `show_id`;
- conversão de `date_added` para data;
- tratamento de valores nulos;
- criação das colunas derivadas `duration_value`, `duration_unit`, `year_added`, `month_added`, `is_movie` e `title_length`;
- criação das tabelas auxiliares `genres.parquet` e `countries.parquet`;
- armazenamento dos dados tratados em `data/processed/`.

Para executar o ETL:

```bash
python src/etl.py
```

Arquivos gerados:

```txt
data/processed/netflix_clean.parquet
data/processed/genres.parquet
data/processed/countries.parquet
```

Para executar o dashboard localmente:

```bash
streamlit run dashboard/app.py
```

## 📚 Referências

- [Kaggle – Netflix Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- [Pandas docs](https://pandas.pydata.org/docs/)
- [Streamlit docs](https://docs.streamlit.io/)
