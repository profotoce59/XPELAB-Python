"""Exercise 3 - the two together, on a question that hides a trap.

    python -m src.exercises.pandas_and_duckdb

The question: for each decade, which 3 films returned the most money
compared to what they cost?

pandas and DuckDB are not rivals. DuckDB can query a DataFrame that is
already in memory and hand the result back as a DataFrame, so you pick
whichever expresses each step more clearly.
"""

import duckdb
import pandas as pd

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    movies = pd.read_csv(MOVIES_CSV)

    print("=== DuckDB reads a DataFrame by variable name ===")
    # `movies` below is the Python variable. DuckDB finds it in the calling
    # scope and reads its memory directly - no copy, no export step.
    n = duckdb.sql("SELECT COUNT(*) FROM movies").fetchone()[0]
    print(f"  SELECT COUNT(*) FROM movies  ->  {n:,}")
    result = duckdb.sql("SELECT genre, COUNT(*) AS films FROM movies GROUP BY 1 ORDER BY 2 DESC LIMIT 3").df()
    print(f"  and .df() hands the result back as a {type(result).__name__}:")
    print(result.to_string(index=False))
    print()

    print("=== THE TRAP: 28 % of the budgets are missing ===")
    missing = movies["budget"].isna().sum()
    print(f"  films with no budget : {missing:,} / {len(movies):,}")
    print("  We want ROI = gross / budget. Watch what the shortcut does.\n")

    naive = movies.copy()
    naive["budget"] = naive["budget"].fillna(0)      # the tempting one-liner
    naive["roi"] = naive["gross"] / naive["budget"]
    infinite = naive["roi"].isin([float("inf"), float("-inf")]).sum()
    print(f"  after fillna(0), ROI is infinite for {infinite:,} films")
    print("  Dividing by a budget of zero gives inf, and inf sorts above")
    print("  everything. The top of your ranking is now pure noise:")
    print(naive.nlargest(3, "roi")[["name", "year", "budget", "gross", "roi"]].to_string(index=False))
    print("\n  fillna(0) did not fill a hole, it invented a fact.")
    print("  'unknown budget' and 'zero budget' are different things.\n")

    print("=== The honest version: keep only what we can actually compute ===")
    usable = movies.dropna(subset=["budget", "gross"]).copy()
    usable["roi"] = usable["gross"] / usable["budget"]
    usable["decade"] = usable["year"] // 10 * 10
    print(f"  {len(usable):,} films have both a budget and a box office")
    print(f"  ({100 * len(usable) / len(movies):.0f} % of the file - and we say so in the result)\n")

    print("=== The question, in SQL over the cleaned DataFrame ===")
    # pandas did the cleaning, which is awkward in SQL.
    # SQL does the ranking, which is awkward in pandas.
    top3 = duckdb.sql("""
        SELECT decade, name, director,
               budget, gross,
               ROUND(roi, 1) AS roi
        FROM usable
        QUALIFY ROW_NUMBER() OVER (PARTITION BY decade ORDER BY roi DESC, name) <= 3
        ORDER BY decade, roi DESC
    """).df()
    print(top3.to_string(index=False))
    print()
    print("  ROW_NUMBER() OVER (PARTITION BY decade ORDER BY roi DESC) numbers")
    print("  the films 1, 2, 3... restarting at each decade; QUALIFY keeps the")
    print("  first three. The tie-break on `name` makes the result reproducible.\n")

    print("=== The same thing in pandas, for comparison ===")
    pandas_top3 = (
        usable.sort_values(["roi", "name"], ascending=[False, True])
        .groupby("decade")
        .head(3)
        .sort_values(["decade", "roi"], ascending=[True, False])
    )
    same = set(zip(top3["decade"], top3["name"])) == set(zip(pandas_top3["decade"], pandas_top3["name"]))
    print(f"  identical results: {same}")
    print("  It works, but the intent is buried in the order of the steps:")
    print("  you must sort BEFORE grouping for head(3) to mean 'top 3'.")
    print("  This is the point where SQL earns its place.\n")

    print("=== Does the missing data change the conclusion? ===")
    # Always ask this. Dropping rows is a choice, not a neutral act.
    for label, frame in (("all films", movies), ("films with a budget", usable)):
        by_decade = frame.groupby(frame["year"] // 10 * 10)["score"].mean()
        print(f"  mean IMDb score, {label:20}: "
              + "  ".join(f"{d}s {v:.2f}" for d, v in by_decade.items()))
    print("  The films with a known budget score slightly differently - they")
    print("  are the bigger productions. Dropping rows is never neutral.\n")

    print("=== À toi de jouer ===")
    print("  1. Les 3 plus gros échecs financiers de chaque décennie.")
    print("     (un film qui perd de l'argent a un roi < 1)")
    print("  2. Un gros budget donne-t-il une meilleure note ?")
    print("     (piste : usable[['budget', 'score']].corr())")
    print("  3. Quel genre a le meilleur ROI MÉDIAN ?")
    print("     Compare avec le classement par moyenne : pourquoi diffèrent-ils ?")
    print()
    print("  Corrigé : python -m src.correctif.03_pandas_and_duckdb")


if __name__ == "__main__":
    main()
