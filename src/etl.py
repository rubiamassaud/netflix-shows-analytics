from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "netflix_titles.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed"


def load_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Carrega o CSV bruto da Netflix."""
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}\n"
            "Coloque o arquivo netflix_titles.csv dentro de data/raw/."
        )
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e padroniza o dataset principal."""
    df = df.copy()

    # Padronização dos nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Padronização de textos
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Remoção de duplicados pela chave do dataset
    if "show_id" in df.columns:
        df = df.drop_duplicates(subset="show_id")
    else:
        df = df.drop_duplicates()

    # Conversão de datas
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    # Tratamento de nulos em colunas categóricas importantes
    fill_values = {
        "country": "Unknown",
        "director": "Unknown",
        "cast": "Unknown",
        "rating": "Not Rated",
        "listed_in": "Unknown",
        "duration": "Unknown",
    }
    for col, value in fill_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)

    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas derivadas usadas nas análises e no dashboard."""
    df = df.copy()

    duration_split = df["duration"].astype(str).str.extract(r"^(\d+)\s+(\w+)")
    df["duration_value"] = pd.to_numeric(duration_split[0], errors="coerce").astype("Int64")
    df["duration_unit"] = duration_split[1].str.lower().map(
        lambda x: "seasons" if isinstance(x, str) and x.startswith("season") else "minutes"
    )

    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")
    df["is_movie"] = df["type"].eq("Movie")
    df["title_length"] = df["title"].astype(str).str.len()

    return df


def create_genres_table(df: pd.DataFrame) -> pd.DataFrame:
    """Cria tabela auxiliar com uma linha por gênero de cada título."""
    return (
        df[["show_id", "listed_in"]]
        .dropna()
        .assign(listed_in=lambda data: data["listed_in"].astype(str).str.split(","))
        .explode("listed_in")
        .assign(genre=lambda data: data["listed_in"].str.strip())
        .drop(columns="listed_in")
        .query("genre != ''")
        .reset_index(drop=True)
    )


def create_countries_table(df: pd.DataFrame) -> pd.DataFrame:
    """Cria tabela auxiliar com uma linha por país de cada título."""
    return (
        df[["show_id", "country"]]
        .dropna()
        .assign(country=lambda data: data["country"].astype(str).str.split(","))
        .explode("country")
        .assign(country=lambda data: data["country"].str.strip())
        .query("country != ''")
        .reset_index(drop=True)
    )


def save_parquet(df: pd.DataFrame, name: str) -> Path:
    """Salva um DataFrame em Parquet na pasta data/processed."""
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_PATH / f"{name}.parquet"
    df.to_parquet(output_path, index=False)
    return output_path


def run_etl() -> dict[str, Path]:
    """Executa o pipeline completo e retorna os caminhos gerados."""
    df = load_data()
    df_clean = clean_data(df)
    df_clean = add_derived_columns(df_clean)

    genres = create_genres_table(df_clean)
    countries = create_countries_table(df_clean)

    outputs = {
        "netflix_clean": save_parquet(df_clean, "netflix_clean"),
        "genres": save_parquet(genres, "genres"),
        "countries": save_parquet(countries, "countries"),
    }
    return outputs


def main() -> None:
    outputs = run_etl()
    print("ETL finalizado com sucesso!")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
