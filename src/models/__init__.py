"""The `models` package.

An `__init__.py` marks a folder as a package. Keep it to re-exports so
that the code lives in a file you can find by name, while callers can
still write `from src.models import Movie`.
"""

from src.models.movie import Movie

__all__ = ["Movie"]
