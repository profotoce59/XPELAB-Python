"""Corrigé de l'exercice 1 - pandas.

    python -m src.correctif.01_pandas_intro
"""

import pandas as pd

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    movies = pd.read_csv(MOVIES_CSV)

    print("=== 1. Quel pays produit les films les mieux notés (min. 20 films) ? ===")
    # Le minimum de films est le coeur de la question : sans lui, un pays
    # avec un seul film très bien noté arrive en tête, ce qui ne veut rien dire.
    pays = (
        movies.groupby("country")
        .agg(films=("name", "size"), note_moyenne=("score", "mean"))
        .reset_index()
    )
    top = pays[pays["films"] >= 20].sort_values("note_moyenne", ascending=False)
    print(top.head(5).round(2).to_string(index=False))

    sans_filtre = pays.sort_values("note_moyenne", ascending=False).head(3)
    print("\n  Sans le filtre des 20 films, on obtiendrait :")
    print(sans_filtre.round(2).to_string(index=False))
    print("  -> des pays à 1 ou 2 films. Le classement ne mesure plus rien.\n")

    print("=== 2. La durée moyenne a-t-elle changé depuis 1980 ? ===")
    movies["decennie"] = movies["year"] // 10 * 10
    duree = (
        movies.groupby("decennie")
        .agg(duree_moyenne=("runtime", "mean"), films=("name", "size"))
        .round(1)
    )
    print(duree.to_string())

    debut = duree.loc[1980, "duree_moyenne"]
    fin = duree.loc[2010, "duree_moyenne"]
    print(f"\n  1980 : {debut} min  ->  2010 : {fin} min  "
          f"({fin - debut:+.1f} min)")
    print("  On compare 1980 à 2010, pas à 2020 : la décennie 2020 ne contient")
    print(f"  que {duree.loc[2020, 'films']:.0f} films, sa moyenne n'est pas comparable.")
    print("  Regarder la taille des groupes avant de conclure est un réflexe.\n")

    print("=== 3. Quel studio apparaît le plus souvent ? ===")
    # value_counts est la façon la plus directe de répondre.
    print(movies["company"].value_counts().head(5).to_string())
    manquants = movies["company"].isna().sum()
    print(f"\n  ({manquants} films n'ont pas de studio renseigné ; value_counts")
    print("   les ignore silencieusement, ce qui est le bon comportement ici.)")


if __name__ == "__main__":
    main()
