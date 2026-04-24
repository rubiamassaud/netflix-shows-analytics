import pandas as pd
import os
import hashlib

RAW_PATH = "data/raw/netflix_titles.csv"


def gerar_hash(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def validar_csv(path):
    print("=" * 50)
    print("VALIDAÇÃO DO CSV BRUTO — Netflix Shows")
    print("=" * 50)

    # 1. Arquivo existe?
    assert os.path.exists(path), f"❌ Arquivo não encontrado: {path}"
    print(f" Arquivo encontrado: {path}")

    # 2. Hash para rastreabilidade
    print(f" MD5: {gerar_hash(path)}")

    # 3. Leitura
    df = pd.read_csv(path)
    print(f"\n Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")

    # 4. Colunas esperadas
    colunas_esperadas = [
        "show_id", "type", "title", "director", "cast",
        "country", "date_added", "release_year", "rating",
        "duration", "listed_in", "description"
    ]
    colunas_faltando = [c for c in colunas_esperadas if c not in df.columns]
    if colunas_faltando:
        print(f" Colunas faltando: {colunas_faltando}")
    else:
        print(
            f" Todas as {len(colunas_esperadas)} colunas esperadas presentes")

    # 5. Duplicatas
    duplicatas = df.duplicated(subset="show_id").sum()
    print(f"\n Linhas duplicadas (show_id): {duplicatas}")

    # 6. Nulos por coluna
    print("\nValores nulos por coluna:")
    nulos = df.isnull().sum()
    for col, qtd in nulos.items():
        pct = (qtd / len(df)) * 100
        flag = " [ATENCAO: >10%]" if pct > 10 else ""
        print(f"   {col:<15} {qtd:>5} ({pct:.1f}%){flag}")

    # 7. Distribuição de tipos
    print("\n Distribuição de 'type':")
    print(df["type"].value_counts().to_string())

    # 8. Range de anos
    print(
        f"\n release_year: {int(df['release_year'].min())} → {int(df['release_year'].max())}")

    print("\n Validação concluída com sucesso!")
    return df


if __name__ == "__main__":
    validar_csv(RAW_PATH)
