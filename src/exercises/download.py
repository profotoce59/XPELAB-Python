"""Download the CSV the data exercises work on.

    python -m src.exercises.download

7 668 films released between 1980 and 2020, with their budget, box office,
IMDb score, director and genre. 1.3 MB, so this takes a second.

`urllib` ships with Python, so there is nothing to install to run this.
"""

import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/danielgrijalva/movie-stats/master/movies.csv"

ROOT = Path(__file__).resolve().parent.parent.parent
MOVIES_CSV = ROOT / "data" / "movies.csv"


def require_data() -> None:
    """Fail with a useful message instead of a bare FileNotFoundError."""
    if not MOVIES_CSV.exists():
        raise SystemExit(
            "data/movies.csv is missing.\n"
            "Run this first:  python -m src.exercises.download"
        )


def main() -> None:
    MOVIES_CSV.parent.mkdir(exist_ok=True)

    if MOVIES_CSV.exists():
        print(f"movies.csv: already here ({MOVIES_CSV.stat().st_size / 1024:.0f} KB)")
    else:
        print("movies.csv: downloading...")
        urllib.request.urlretrieve(URL, MOVIES_CSV)
        print(f"movies.csv: done ({MOVIES_CSV.stat().st_size / 1024:.0f} KB)")

    print("\nReady. Start with:  python -m src.exercises.pandas_intro")


if __name__ == "__main__":
    main()
