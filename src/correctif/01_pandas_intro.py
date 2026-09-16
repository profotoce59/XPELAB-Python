"""Corrigé de l'exercice 1 - pandas.

    python -m src.correctif.01_pandas_intro
"""

import pandas as pd

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    movies = pd.read_csv(MOVIES_CSV)

    print("=== 0. Découper `released` en date + pays ===")
    # released vaut par exemple "June 13, 1980 (United States)".
    # .str.extract() applique une regex à chaque valeur et renvoie une colonne
    # par groupe capturant. Les groupes nommés (?P<nom>...) donnent leurs noms
    # aux colonnes, ce qui évite de manipuler des numéros.
    parts = movies["released"].str.extract(r"^(?P<date>[^(]+?)\s*\((?P<country>[^)]+)\)$")
    movies["release_country"] = parts["country"]

    # %B = nom complet du mois, %d = jour, %Y = année sur 4 chiffres.
    # errors="coerce" : une valeur illisible devient NaT au lieu de lever
    # une exception et de faire perdre toute la colonne.
    strict = pd.to_datetime(parts["date"], format="%B %d, %Y", errors="coerce")

    # PIÈGE : %B lit le NOM du mois, et pandas le compare aux noms de mois
    # de TA locale. Sur un Python configuré en français, "June" n'est pas
    # reconnu et absolument tout devient NaT. On le détecte au lieu de le subir.
    if strict.notna().sum() == 0:
        print("  %B n'a rien lu : ta locale n'est pas anglaise.")
        print("  On bascule sur format='mixed', qui passe par dateutil et")
        print("  connaît les mois anglais quelle que soit la locale.\n")
        movies["release_date"] = pd.to_datetime(parts["date"], format="mixed", errors="coerce")
    else:
        movies["release_date"] = strict

    print(f"  dtype obtenu : {movies['release_date'].dtype}")
    print(f"  lignes lues  : {movies['release_date'].notna().sum():,} / {len(movies):,}")
    exemple = movies.loc[movies["release_date"].notna()].iloc[0]
    print(f"  exemple : {exemple['released']!r}")
    print(f"         -> {exemple['release_date'].date()} en {exemple['release_country']}")

    ratees = movies[movies["release_date"].isna() & movies["released"].notna()]
    if len(ratees):
        print(f"\n  {len(ratees)} lignes non lues, les trois premières :")
        for valeur in ratees["released"].head(3):
            print(f"    {valeur!r}")
        print("  Elles n'ont pas de jour, parfois pas de mois. Sans")
        print("  errors='coerce', elles auraient fait échouer tout l'appel.")

    # Un parseur plus permissif n'est pas automatiquement meilleur.
    permissif = pd.to_datetime(parts["date"], format="mixed", errors="coerce")
    print(f"\n  À titre de comparaison, format='mixed' lit "
          f"{permissif.notna().sum():,} lignes au lieu de "
          f"{strict.notna().sum():,}.")
    exemple_invente = parts.loc[permissif.notna() & strict.isna(), "date"]
    if len(exemple_invente):
        brut = exemple_invente.iloc[-1]
        print(f"  Mais il INVENTE ce qui manque : {brut!r} devient "
              f"{permissif[exemple_invente.index[-1]].date()}.")
        print("  Un 1er janvier qui n'existe pas dans la source. À choisir en")
        print("  connaissance de cause, pas parce que ça fait moins de NaT.\n")

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
    print("  On compare 1980 à 2010")
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
