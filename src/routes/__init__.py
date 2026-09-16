"""The `routes` package.

An `__init__.py` marks a folder as a package. Keep it to re-exports so
that the code lives in a file you can find by name, while callers can
still write `from src.routes import create_router`.
"""

from src.routes.movies_routes import create_router

__all__ = ["create_router"]
