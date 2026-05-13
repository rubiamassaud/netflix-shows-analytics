import pandas as pd

def test_dataset():
    df = pd.read_parquet(
        "data/processed/netflix_titles_cleaned.parquet"
    )

    assert not df.empty
    assert "type" in df.columns
    assert "release_year" in df.columns
    assert "country" in df.columns
    assert "rating" in df.columns
    assert "duration" in df.columns

    print("Integração ETL ↔ Dashboard OK")

if __name__ == "__main__":
    test_dataset()