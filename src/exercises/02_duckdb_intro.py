"""Exercise 2 - DuckDB: SQL straight onto the CSV file.

    python -m src.exercises.duckdb_intro

DuckDB is a database engine that runs inside your Python process. There is
no server to start and no table to create: it reads a CSV file as if it
were already a table.

The same questions as exercise 1, written as SQL.
"""

import duckdb

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    csv = str(MOVIES_CSV)

    print("=== Querying a file with no import step ===")
    count = duckdb.sql(f"SELECT COUNT(*) FROM '{csv}'").fetchone()
    print(f"  SELECT COUNT(*) FROM 'movies.csv'  ->  {count[0]:,}")
    print("  Nothing was loaded into Python. DuckDB read the file itself.\n")

    print("=== The types DuckDB inferred on its own ===")
    schema = duckdb.sql(f"DESCRIBE SELECT * FROM '{csv}'").df()
    print(schema[["column_name", "column_type"]].to_string(index=False))
    print()

    print("=== A first query ===")
    # .df() hands the result back as a pandas DataFrame.
    best = duckdb.sql(f"""
        SELECT name, year, director, score
        FROM '{csv}'
        ORDER BY score DESC
        LIMIT 5
    """).df()
    print(best.to_string(index=False))
    print()

    print("=== GROUP BY and HAVING ===")
    # WHERE filters rows BEFORE grouping.
    # HAVING filters groups AFTER aggregating - that is the difference,
    # and it is why `WHERE COUNT(*) >= 5` is a syntax error.
    directors = duckdb.sql(f"""
        SELECT director,
               COUNT(*)          AS films,
               ROUND(AVG(score), 2) AS avg_score,
               MAX(score)        AS best
        FROM '{csv}'
        WHERE score IS NOT NULL
        GROUP BY director
        HAVING COUNT(*) >= 5
        ORDER BY avg_score DESC
        LIMIT 5
    """).df()
    print(directors.to_string(index=False))
    print("  Same answer as exercise 1, in one statement instead of a chain.\n")

    print("=== Most common genre per decade ===")
    per_decade = duckdb.sql(f"""
        SELECT (year // 10) * 10 AS decade, genre, COUNT(*) AS films
        FROM '{csv}'
        GROUP BY 1, 2
        QUALIFY ROW_NUMBER() OVER (PARTITION BY decade ORDER BY films DESC) = 1
        ORDER BY decade
    """).df()
    print(per_decade.to_string(index=False))
    print()
    print("  ROW_NUMBER() OVER (PARTITION BY decade ORDER BY films DESC)")
    print("    numbers the rows 1, 2, 3... restarting at each decade.")
    print("  QUALIFY filters on that number. WHERE cannot: the number does")
    print("    not exist yet at that stage. QUALIFY is to window functions")
    print("    what HAVING is to GROUP BY.\n")

    print("=== The trap: integer division is not the same in both languages ===")
    year = 1986
    trap = duckdb.sql(f"""
        SELECT ({year} / 10)::INT * 10 AS cast_int,
               ({year} // 10) * 10     AS floor_div
    """).fetchone()
    print(f"  Python : {year} // 10 * 10        = {year // 10 * 10}")
    print(f"  SQL    : ({year} / 10)::INT * 10  = {trap[0]}   <-- WRONG")
    print(f"  SQL    : ({year} // 10) * 10      = {trap[1]}")
    print("  In DuckDB `/` is floating-point division and `::INT` ROUNDS to the")
    print("  nearest integer: 1986 / 10 = 198.6, rounded to 199 -> the 1990s.")
    print("  Python's `//` truncates, which is what a decade needs.")

    # Do not take this on trust - count how many years actually break.
    wrong = [
        y for y in range(1980, 2021)
        if duckdb.sql(f"SELECT ({y}/10)::INT*10").fetchone()[0] != y // 10 * 10
    ]
    print(f"\n  Over 1980-2020, {len(wrong)} of 41 years land in the wrong decade:")
    print(f"    {wrong[:9]} ...")
    print("  Every year ending in 6, 7, 8 or 9. No error, no warning - just a")
    print("  silently different answer. Use `//` or FLOOR().\n")

    print("=== Two conveniences DuckDB adds to SQL ===")
    trimmed = duckdb.sql(f"SELECT * EXCLUDE (writer, star, company) FROM '{csv}' LIMIT 1").df()
    print(f"  SELECT * EXCLUDE (...)  -> kept: {list(trimmed.columns)}")
    print("  There is also GROUP BY ALL, which groups by every non-aggregated")
    print("  column. Both are DuckDB extensions, not standard SQL.")
    print("  Note: GROUP BY ALL cannot currently be combined with QUALIFY.\n")

    print("=== À toi de jouer ===")
    print("  1. Repose les trois questions de l'exercice 1, mais en SQL.")
    print("  2. Quel genre a la meilleure note moyenne ?")
    print("     Ajoute un minimum de films : le gagnant change-t-il ?")
    print("  3. Exporte le CSV en Parquet, puis compare les deux tailles :")
    print("     COPY (SELECT * FROM 'movies.csv')")
    print("     TO 'data/movies.parquet' (FORMAT PARQUET)")
    print()
    print("  Corrigé : python -m src.correctif.02_duckdb_intro")


if __name__ == "__main__":
    main()
