# Validacao do CSV Bruto

- Fonte: Kaggle - Netflix Shows
- Data da extracao: 25/04/2026
- MD5: 0bc7e8d9621caab0a32f46d054faca7f
- Dimensoes: 8807 linhas x 12 colunas
- Colunas faltando: nenhuma
- Duplicatas: 0
- Observacoes:
  - director: 2634 nulos (29.9%) - esperado, nem todo titulo tem diretor registrado
  - cast: 825 nulos (9.4%) - esperado
  - country: 831 nulos (9.4%) - esperado, sera preenchido com "Unknown" no ETL
  - release_year: range 1925-2021 - valido