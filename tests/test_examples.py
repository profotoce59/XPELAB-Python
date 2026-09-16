"""Unit tests.

Rust puts tests inside the module, in a `#[cfg(test)] mod tests` block.
Python puts them in a separate `tests/` directory, in files named
`test_*.py` containing functions named `test_*`. That naming IS the
registration: pytest discovers them by convention, there is no attribute
to add.

Run: pytest
"""

import pytest

import importlib

from src.errors import XpelabError
from src.models import Movie

# Les fichiers d'exemples sont préfixés par un numéro (01_, 02_, ...) pour
# suivre l'ordre du README. Conséquence : on ne peut PAS écrire
#     from src.examples.03_functions import add
# parce qu'un nom de module ne peut pas commencer par un chiffre. C'est une
# erreur de SYNTAXE, détectée avant même de chercher le fichier.
#
# `python -m src.examples.03_functions` continue de fonctionner : cette forme
# passe par runpy, qui reçoit le nom du module sous forme de chaîne.
# Pour importer depuis du code, il faut faire pareil - importlib prend
# lui aussi une chaîne.
_functions = importlib.import_module("src.examples.03_functions")
_generics = importlib.import_module("src.examples.07_generics")

add = _functions.add
divide = _functions.divide
highest_value = _generics.highest_value


def test_add() -> None:
    # `assert` is a plain statement. pytest rewrites it so that a failure
    # shows both sides of the comparison, the way `assert_eq!` does.
    assert add(2, 3) == 5


def test_divide_returns_none_on_zero() -> None:
    assert divide(10.0, 2.0) == 5.0
    assert divide(10.0, 0.0) is None


def test_highest_value() -> None:
    assert highest_value([10, 20, 5]) == 20
    assert highest_value([]) is None


def test_raises() -> None:
    """`pytest.raises` asserts that an exception IS raised."""
    with pytest.raises(XpelabError, match="boom"):
        raise XpelabError("boom")


# `parametrize` runs the same test with several sets of inputs.
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(1, 1, 2), (0, 0, 0), (-1, 1, 0), (100, 200, 300)],
)
def test_add_parametrized(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected


def test_movie_model_validates() -> None:
    """pydantic validates at runtime - what the Rust compiler does statically."""
    movie = Movie(title="Matrix", director="Wachowski", release_year=1999)
    assert movie.id is None
    assert movie.model_dump() == {
        "id": None,
        "title": "Matrix",
        "director": "Wachowski",
        "release_year": 1999,
    }

    with pytest.raises(ValueError):
        Movie(title="Matrix", director="Wachowski", release_year="not a year")  # type: ignore[arg-type]


@pytest.fixture
def sample_movie() -> Movie:
    """A fixture: reusable setup, injected by name into any test."""
    return Movie.new(1, "Matrix", "Wachowski", 1999)


def test_with_fixture(sample_movie: Movie) -> None:
    assert sample_movie.id == 1
    assert sample_movie.title == "Matrix"
