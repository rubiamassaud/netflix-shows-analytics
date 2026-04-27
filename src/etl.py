import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "netflix_titles.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed"

def load_data():
    return pd.read_csv(RAW_PATH)

def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.lower()

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    df = df.drop_duplicates(subset="show_id")

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

    df["country"] = df["country"].fillna("Unknown")
    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Not Rated")

    return df


def add_derived_columns(df):
    df = df.copy()

    duration_split = df["duration"].str.extract(r"^(\d+)\s+(\w+)")
    df["duration_value"] = pd.to_numeric(duration_split[0], errors="coerce").astype("Int64")
    df["duration_unit"] = duration_split[1].str.lower().map(
        lambda x: "seasons" if isinstance(x, str) and x.startswith("season") else "minutes"
    )

    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")
    df["is_movie"] = df["type"] == "Movie"
    df["title_length"] = df["title"].str.len()

    return df


def create_genres_table(df):
    return (
        df[['show_id', 'listed_in']]
        .dropna()
        .assign(listed_in=lambda x: x['listed_in'].str.split(', '))
        .explode('listed_in')
        .rename(columns={'listed_in': 'genre'})
    )

def create_countries_table(df):
    return (
        df[['show_id', 'country']]
        .dropna()
        .assign(country=lambda x: x['country'].str.split(', '))
        .explode('country')
    )

def save_parquet(df, name):
    output_path = PROCESSED_PATH / f"{name}.parquet"
    df.to_parquet(output_path, index=False)

def main():
    df = load_data()
    df = clean_data(df)
    df = add_derived_columns(df)

    genres = create_genres_table(df)
    countries = create_countries_table(df)

    save_parquet(df, "netflix_clean")
    save_parquet(genres, "genres")
    save_parquet(countries, "countries")

    print("ETL finalizado!")

if __name__ == "__main__":
    main()
