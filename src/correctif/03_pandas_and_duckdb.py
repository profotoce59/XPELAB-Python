"""Corrigé de l'exercice 3 - pandas et DuckDB ensemble.

    python -m src.correctif.03_pandas_and_duckdb
"""

import duckdb
import pandas as pd

from src.exercises.download import MOVIES_CSV, require_data


def main() -> None:
    require_data()
    movies = pd.read_csv(MOVIES_CSV)

    # Le nettoyage de l'exercice : on ne garde que les films dont on peut
    # réellement calculer le rapport recettes / budget.
    usable = movies.dropna(subset=["budget", "gross"]).copy()
    usable["roi"] = usable["gross"] / usable["budget"]
    usable["decennie"] = usable["year"] // 10 * 10

    print("=== 1. Les 3 plus gros échecs financiers par décennie ===")
    # Même requête que le top 3, avec l'ordre inversé et un filtre roi < 1.
    # roi < 1 = le film a rapporté moins qu'il n'a coûté.
    echecs = duckdb.sql("""
        SELECT decennie, name, director,
               budget, gross,
               ROUND(roi, 3) AS roi
        FROM usable
        WHERE roi < 1
        QUALIFY ROW_NUMBER() OVER (PARTITION BY decennie ORDER BY roi ASC, name) <= 3
        ORDER BY decennie, roi ASC
    """).df()
    print(echecs.to_string(index=False))
    perdants = (usable["roi"] < 1).sum()
    print(f"\n  {perdants:,} films sur {len(usable):,} ont perdu de l'argent "
          f"({100 * perdants / len(usable):.0f} %).")
    print("  Attention : `gross` ne compte que les entrées en salle. Un film")
    print("  peut être rentable via la VOD et les droits TV. Le chiffre dit")
    print("  ce qu'il mesure, pas plus.\n")

    print("=== 2. Un gros budget donne-t-il une meilleure note ? ===")
    correlation = usable[["budget", "score", "gross", "votes"]].corr()
    print(correlation.round(3).to_string())
    r = correlation.loc["budget", "score"]
    print(f"\n  corrélation budget / score : {r:.3f}")
    print("  Proche de zéro : le budget n'explique pratiquement pas la note.")
    print(f"  En revanche budget / gross vaut {correlation.loc['budget', 'gross']:.3f} :")
    print("  les gros budgets font des grosses recettes, sans faire de bons films.")
    print("\n  Rappel : une corrélation n'est pas une cause, et .corr() ne mesure")
    print("  qu'une relation LINÉAIRE. Un lien en cloche donnerait 0 aussi.\n")

    print("=== 3. Le meilleur ROI par genre : médiane ou moyenne ? ===")
    par_genre = (
        usable.groupby("genre")
        .agg(films=("name", "size"), roi_moyen=("roi", "mean"), roi_median=("roi", "median"))
        .reset_index()
    )
    par_genre = par_genre[par_genre["films"] >= 30]

    print("  Classement par MOYENNE :")
    print(par_genre.sort_values("roi_moyen", ascending=False).head(3).round(2).to_string(index=False))
    print("\n  Classement par MÉDIANE :")
    print(par_genre.sort_values("roi_median", ascending=False).head(3).round(2).to_string(index=False))

    horreur = usable[usable["genre"] == "Horror"]
    print(f"\n  Pourquoi la médiane ? Regardons le genre Horror ({len(horreur)} films) :")
    print(f"    ROI moyen   : {horreur['roi'].mean():8.1f}")
    print(f"    ROI médian  : {horreur['roi'].median():8.1f}")
    pire = horreur.nlargest(1, "roi")
    print(f"    film le plus extrême : {pire['name'].iloc[0]} à x{pire['roi'].iloc[0]:.0f}")
    sans_extreme = horreur.nsmallest(len(horreur) - 1, "roi")["roi"].mean()
    print(f"    moyenne sans ce seul film : {sans_extreme:.1f}")
    print("\n  Un seul film déplace la moyenne de tout un genre. La médiane ne")
    print("  bouge pas : c'est la valeur du film du milieu, quel que soit")
    print("  l'extrême au-dessus.")
    print("  Règle : sur une grandeur très étalée (ROI, salaires, temps de")
    print("  réponse), la moyenne décrit mal. Utiliser la médiane.")


if __name__ == "__main__":
    main()
