"""Exercise 1 - pandas: load a CSV, clean it, ask it questions.

    python -m src.exercises.pandas_intro

pandas loads a file into memory as a `DataFrame`: a table with named
columns. It is the standard tool for cleaning and reshaping data in Python.
"""

import pandas as pd

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()

    # read_csv guesses the separator, the header row and every column type.
    movies = pd.read_csv(MOVIES_CSV)

    print("=== What did we just load? ===")
    print(f"  shape (rows, columns) : {movies.shape}")
    print(f"  columns               : {list(movies.columns)}\n")

    # head() is how you look at data. Never print a whole DataFrame.
    print(movies.head(3)[["name", "year", "genre", "score", "budget", "gross"]].to_string(index=False))

    print("=== Where the holes are ===")
    holes = movies.isna().sum()
    print(holes[holes > 0].to_string())
    print(f"\n  budget is missing for {movies['budget'].isna().sum():,} films "
          f"({100 * movies['budget'].isna().mean():.0f} %).")
    print("  That one matters - see exercise 3.\n")

    print("=== A column is a Series ===")
    # A DataFrame is a dict of Series. A Series is a 1-D array with an index.
    print(f"  type(movies)           : {type(movies).__name__}")
    print(f"  type(movies['genre'])  : {type(movies['genre']).__name__}")
    print(f"  distinct genres        : {movies['genre'].nunique()}")
    print(f"  distinct directors     : {movies['director'].nunique():,}\n")

    print("  Films per genre (top 5):")
    # value_counts answers "how often does each value appear?"
    print(movies["genre"].value_counts().head(5).to_string())
    print()

    print("=== Nettoyage : une date avec un pays collé dedans ===")
    valeur = movies["released"].dropna().iloc[0]
    print(f"  valeur brute : {valeur!r}")
    print(f"  type         : {type(valeur).__name__}   -> du texte, pas une date")
    print()
    print("  À toi : extrais de `released` deux nouvelles colonnes")
    print("    - release_date    : un vrai datetime")
    print("    - release_country : le pays, sans les parenthèses")
    print("  Pistes : .str.extract() avec une regex, puis pd.to_datetime()")
    print("  Attention : certaines lignes ne suivent pas le format. Utilise")
    print("  errors='coerce' pour qu'elles deviennent NaT au lieu de tout casser.")
    print("  Vérifie : movies['release_date'].dtype doit valoir datetime64[ns]")
    print("  Si tu obtiens QUE des NaT : %B lit le nom du mois dans la langue")
    print("  de ta locale. Essaie format='mixed' et lis le corrigé.")
    print()

    # ... ton code ici ...

    print("=== Selecting rows: a boolean mask ===")
    # The mask is a Series of True/False, one per row.
    recent = movies[movies["year"] >= 2010]
    print(f"  movies['year'] >= 2010  ->  {len(recent):,} films")

    # Combine with & | ~ and parenthesise each condition.
    # Using `and` raises
    good_and_recent = movies[(movies["year"] >= 2010) & (movies["score"] >= 8)]
    print(f"  year >= 2010 AND score >= 8  ->  {len(good_and_recent):,} films")
    try:
        _ = movies["year"] >= 2010 and movies["score"] >= 8
    except ValueError as error:
        print(f"  using `and` instead of `&`: ValueError: {str(error)[:52]}...\n")

    print("=== Grouping: the heart of pandas ===")
    # groupby splits into groups, computes per group, glues results back.
    # .agg(name=(column, function)) names the output columns for you.
    directors = (
        movies.groupby("director")
        .agg(
            films=("name", "size"),
            avg_score=("score", "mean"),
            best=("score", "max"),
        )
        .reset_index()            # turn the group key back into a column
    )
    print(f"  {len(directors):,} directors\n")

    print("  Best directors, minimum 5 films:")
    # Filtering AFTER aggregating is what stops one-hit wonders winning.
    frequent = directors[directors["films"] >= 5]
    print(
        frequent.sort_values("avg_score", ascending=False)
        .head(5)
        .round(2)
        .to_string(index=False)
    )
    print()

    print("=== Two group keys ===")
    movies["decade"] = movies["year"] // 10 * 10
    per_decade = (
        movies.groupby(["decade", "genre"])
        .size()
        .reset_index(name="films")
    )
    top_genre = (
        per_decade.sort_values("films", ascending=False)
        .groupby("decade")
        .head(1)
        .sort_values("decade")
    )
    print("  Most common genre of each decade:")
    print(top_genre.to_string(index=False))
    print()

    ##=== À toi de jouer ===
    ##  1. Quel pays produit les films les mieux notés ?
    ## garde uniquement les pays ayant au moins 20 films
    
    
    ## 2. Obtenir La durée moyenne des films des années 80 et des années 2010?
    
    
    
    ##3. Quel studio (colonne `company`) revient le plus souvent ?
    ## Corrigé : python -m src.correctif.01_pandas_intro


if __name__ == "__main__":
    main()
