from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="Netflix Shows Analytics",
    page_icon="🎬",
    layout="wide",
)


@st.cache_data
def load_processed_data():
    netflix_path = PROCESSED_PATH / "netflix_clean.parquet"
    genres_path = PROCESSED_PATH / "genres.parquet"
    countries_path = PROCESSED_PATH / "countries.parquet"

    missing = [path.name for path in [netflix_path, genres_path, countries_path] if not path.exists()]
    if missing:
        st.error(
            "Arquivos processados não encontrados: "
            + ", ".join(missing)
            + ". Rode primeiro: python src/etl.py"
        )
        st.stop()

    df = pd.read_parquet(netflix_path)
    genres = pd.read_parquet(genres_path)
    countries = pd.read_parquet(countries_path)
    return df, genres, countries


def apply_filters(df, genres, countries):
    st.sidebar.header("Filtros")

    type_options = sorted(df["type"].dropna().unique())
    selected_types = st.sidebar.multiselect("Tipo", type_options, default=type_options)

    years = sorted(df["release_year"].dropna().astype(int).unique())
    min_year, max_year = int(min(years)), int(max(years))
    selected_years = st.sidebar.slider("Ano de lançamento", min_year, max_year, (min_year, max_year))

    genre_options = sorted(genres["genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect("Gênero", genre_options)

    country_options = sorted(countries["country"].dropna().unique())
    selected_countries = st.sidebar.multiselect("País", country_options)

    filtered = df[
        df["type"].isin(selected_types)
        & df["release_year"].between(selected_years[0], selected_years[1])
    ].copy()

    if selected_genres:
        show_ids = genres[genres["genre"].isin(selected_genres)]["show_id"].unique()
        filtered = filtered[filtered["show_id"].isin(show_ids)]

    if selected_countries:
        show_ids = countries[countries["country"].isin(selected_countries)]["show_id"].unique()
        filtered = filtered[filtered["show_id"].isin(show_ids)]

    return filtered


def main():
    st.title("🎬 Netflix Shows Analytics")
    st.write("Dashboard interativo com dados tratados pelo pipeline ETL em Pandas.")

    df, genres, countries = load_processed_data()
    filtered = apply_filters(df, genres, countries)

    filtered_genres = genres[genres["show_id"].isin(filtered["show_id"])]
    filtered_countries = countries[countries["show_id"].isin(filtered["show_id"])]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Títulos", f"{len(filtered):,}".replace(",", "."))
    col2.metric("Filmes", f"{filtered['type'].eq('Movie').sum():,}".replace(",", "."))
    col3.metric("Séries", f"{filtered['type'].eq('TV Show').sum():,}".replace(",", "."))
    col4.metric("Países", filtered_countries["country"].nunique())

    st.divider()

    left, right = st.columns(2)

    with left:
        type_count = filtered["type"].value_counts().reset_index()
        type_count.columns = ["type", "count"]
        st.plotly_chart(
            px.bar(type_count, x="type", y="count", title="Quantidade por tipo", text="count"),
            use_container_width=True,
        )

    with right:
        rating_count = filtered["rating"].value_counts().head(10).reset_index()
        rating_count.columns = ["rating", "count"]
        st.plotly_chart(
            px.pie(rating_count, names="rating", values="count", title="Distribuição de ratings"),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:
        top_genres = filtered_genres["genre"].value_counts().head(10).reset_index()
        top_genres.columns = ["genre", "count"]
        st.plotly_chart(
            px.bar(top_genres, x="count", y="genre", orientation="h", title="Top 10 gêneros"),
            use_container_width=True,
        )

    with right:
        releases = (
            filtered.groupby("release_year")
            .size()
            .reset_index(name="count")
            .sort_values("release_year")
        )
        st.plotly_chart(
            px.line(releases, x="release_year", y="count", markers=True, title="Lançamentos ao longo dos anos"),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:
        top_countries = filtered_countries["country"].value_counts().head(15).reset_index()
        top_countries.columns = ["country", "count"]
        st.plotly_chart(
            px.bar(top_countries, x="country", y="count", title="Top 15 países"),
            use_container_width=True,
        )

    with right:
        duration_df = filtered.dropna(subset=["duration_value"])
        st.plotly_chart(
            px.box(duration_df, x="type", y="duration_value", title="Distribuição de duração por tipo"),
            use_container_width=True,
        )

    st.subheader("Dados filtrados")
    st.dataframe(
        filtered[["show_id", "title", "type", "release_year", "rating", "duration", "country"]],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
