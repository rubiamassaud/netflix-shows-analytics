import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Netflix Shows Analytics",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix Shows Analytics Dashboard")
st.markdown("Dashboard analítico do catálogo Netflix")

# CARREGAMENTO DOS DADOS

@st.cache_data
def load_data():
    df = pd.read_parquet(
        "data/processed/netflix_titles_cleaned.parquet"
    )
    return df

df = load_data()

# SIDEBAR FILTROS

st.sidebar.header("Filtros")

tipo = st.sidebar.multiselect(
    "Tipo",
    options=df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
)

anos = st.sidebar.slider(
    "Ano de Lançamento",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (
        int(df["release_year"].min()),
        int(df["release_year"].max())
    )
)

paises = st.sidebar.multiselect(
    "País",
    options=sorted(df["country"].dropna().unique()),
    default=[]
)

ratings = st.sidebar.multiselect(
    "Classificação",
    options=df["rating"].dropna().unique(),
    default=df["rating"].dropna().unique()
)

# APLICAÇÃO DOS FILTROS

df_filtered = df[
    (df["type"].isin(tipo)) &
    (df["release_year"].between(anos[0], anos[1])) &
    (df["rating"].isin(ratings))
]

if paises:
    df_filtered = df_filtered[
        df_filtered["country"].isin(paises)
    ]

# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Títulos",
    len(df_filtered)
)

col2.metric(
    "Filmes",
    len(df_filtered[df_filtered["type"] == "Movie"])
)

col3.metric(
    "Séries",
    len(df_filtered[df_filtered["type"] == "TV Show"])
)

st.divider()

# GRÁFICO 1 — TIPO DE CONTEÚDO

st.subheader("1. Distribuição por Tipo")

fig1 = px.pie(
    df_filtered,
    names="type",
    title="Filmes vs Séries"
)

st.plotly_chart(fig1, use_container_width=True)

# GRÁFICO 2 — TOP GÊNEROS

st.subheader("2. Top Gêneros")

genre_count = (
    df_filtered["listed_in"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

fig2 = px.bar(
    x=genre_count.values,
    y=genre_count.index,
    orientation="h",
    labels={
        "x": "Quantidade",
        "y": "Gênero"
    },
    title="Top 10 Gêneros"
)

st.plotly_chart(fig2, use_container_width=True)

# GRÁFICO 3 — LANÇAMENTOS POR ANO

st.subheader("3. Lançamentos por Ano")

release_year = (
    df_filtered["release_year"]
    .value_counts()
    .sort_index()
)

fig3 = px.line(
    x=release_year.index,
    y=release_year.values,
    labels={
        "x": "Ano",
        "y": "Quantidade"
    },
    title="Lançamentos por Ano"
)

st.plotly_chart(fig3, use_container_width=True)

# GRÁFICO 4 — CLASSIFICAÇÃO INDICATIVA

st.subheader("4. Ratings")

rating_count = (
    df_filtered["rating"]
    .value_counts()
)

fig4 = px.bar(
    x=rating_count.index,
    y=rating_count.values,
    labels={
        "x": "Rating",
        "y": "Quantidade"
    },
    title="Distribuição de Ratings"
)

st.plotly_chart(fig4, use_container_width=True)

# GRÁFICO 5 — TOP PAÍSES

st.subheader("5. Top Países")

country_count = (
    df_filtered["country"]
    .value_counts()
    .head(10)
)

fig5 = px.bar(
    x=country_count.values,
    y=country_count.index,
    orientation="h",
    labels={
        "x": "Quantidade",
        "y": "País"
    },
    title="Top 10 Países"
)

st.plotly_chart(fig5, use_container_width=True)

# GRÁFICO 6 — DURAÇÃO

st.subheader("6. Distribuição de Duração")

duration = (
    df_filtered["duration"]
    .value_counts()
    .head(15)
)

fig6 = px.bar(
    x=duration.index,
    y=duration.values,
    labels={
        "x": "Duração",
        "y": "Quantidade"
    },
    title="Distribuição de Duração"
)

st.plotly_chart(fig6, use_container_width=True)

# TABELA FINAL

st.subheader("Dados Filtrados")

st.dataframe(df_filtered)