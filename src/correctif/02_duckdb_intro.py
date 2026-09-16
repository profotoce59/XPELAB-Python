"""Corrigé de l'exercice 2 - DuckDB.

    python -m src.correctif.02_duckdb_intro
"""

import duckdb

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    csv = str(MOVIES_CSV)
    parquet = MOVIES_CSV.with_suffix(".parquet")

    print("=== 1a. Le pays le mieux noté (min. 20 films) ===")
    # HAVING filtre les GROUPES après agrégation.
    # WHERE filtrerait les LIGNES avant, et `WHERE COUNT(*) >= 20`
    # est une erreur de syntaxe.
    print(duckdb.sql(f"""
        SELECT country,
               COUNT(*)              AS films,
               ROUND(AVG(score), 2)  AS note_moyenne
        FROM '{csv}'
        WHERE country IS NOT NULL
        GROUP BY country
        HAVING COUNT(*) >= 20
        ORDER BY note_moyenne DESC
        LIMIT 5
    """).df().to_string(index=False))

    print("\n=== 1b. La durée moyenne par décennie ===")
    # `//` et non `/` : voir le piège de l'exercice.
    print(duckdb.sql(f"""
        SELECT (year // 10) * 10        AS decennie,
               ROUND(AVG(runtime), 1)   AS duree_moyenne,
               COUNT(*)                 AS films
        FROM '{csv}'
        GROUP BY 1
        ORDER BY 1
    """).df().to_string(index=False))

    print("\n=== 1c. Le studio le plus fréquent ===")
    print(duckdb.sql(f"""
        SELECT company, COUNT(*) AS films
        FROM '{csv}'
        WHERE company IS NOT NULL
        GROUP BY company
        ORDER BY films DESC
        LIMIT 5
    """).df().to_string(index=False))

    print("\n=== 2. Le genre le mieux noté, avec et sans minimum ===")
    sans_minimum = duckdb.sql(f"""
        SELECT genre, COUNT(*) AS films, ROUND(AVG(score), 2) AS note
        FROM '{csv}'
        GROUP BY genre
        ORDER BY note DESC
        LIMIT 3
    """).df()
    print("  Sans minimum :")
    print(sans_minimum.to_string(index=False))

    avec_minimum = duckdb.sql(f"""
        SELECT genre, COUNT(*) AS films, ROUND(AVG(score), 2) AS note
        FROM '{csv}'
        GROUP BY genre
        HAVING COUNT(*) >= 50
        ORDER BY note DESC
        LIMIT 3
    """).df()
    print("\n  Avec au moins 50 films :")
    print(avec_minimum.to_string(index=False))

    gagnant_change = sans_minimum["genre"].iloc[0] != avec_minimum["genre"].iloc[0]
    print(f"\n  Le gagnant change : {gagnant_change}")
    print(f"  {sans_minimum['genre'].iloc[0]} ne compte que "
          f"{sans_minimum['films'].iloc[0]} film(s) : une moyenne sur si peu")
    print("  de valeurs n'est pas une mesure, c'est une anecdote.\n")

    print("=== 3. Export en Parquet et comparaison des tailles ===")
    duckdb.sql(f"COPY (SELECT * FROM '{csv}') TO '{parquet}' (FORMAT PARQUET)")

    taille_csv = MOVIES_CSV.stat().st_size / 1024
    taille_parquet = parquet.stat().st_size / 1024
    print(f"  movies.csv     : {taille_csv:7.0f} Ko")
    print(f"  movies.parquet : {taille_parquet:7.0f} Ko  "
          f"({100 * (1 - taille_parquet / taille_csv):.0f} % plus petit)")

    lignes = duckdb.sql(f"SELECT COUNT(*) FROM '{parquet}'").fetchone()[0]
    print(f"  et il se relit pareil : SELECT COUNT(*) -> {lignes:,}")
    print("\n  Parquet stocke colonne par colonne : les valeurs qui se répètent")
    print("  se compressent bien, et les types sont écrits dans le fichier -")
    print("  plus de détection à refaire à chaque lecture.")
    print("  Réflexe : dès qu'un CSV est lu plus d'une fois, le convertir.")


if __name__ == "__main__":
    main()
