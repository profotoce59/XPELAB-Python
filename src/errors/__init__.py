"""The `errors` package.

An `__init__.py` marks a folder as a package. Keep it to re-exports so
that the code lives in a file you can find by name, while callers can
still write `from src.errors import XpelabError`.
"""

from src.errors.xpelab_error import XpelabError

__all__ = ["XpelabError"]
