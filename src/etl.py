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

    genres = create_genres_table(df)
    countries = create_countries_table(df)

    save_parquet(df, "netflix_clean")
    save_parquet(genres, "genres")
    save_parquet(countries, "countries")

    print("ETL finalizado!")

if __name__ == "__main__":
    main()
