"""Data models.

Rust uses a `struct` plus `#[derive(Serialize, Deserialize)]` to convert
to/from JSON. In Python, pydantic plays both roles: it describes the shape
AND validates/serializes it at runtime.
"""

from pydantic import BaseModel


class Movie(BaseModel):
    """A movie.

    `id` is optional: it does not exist yet when the movie is created.
    This is the equivalent of Rust's `Option<u32>`; in Python we write
    `int | None` and give a default value of `None`.
    """

    id: int | None = None
    title: str
    director: str
    release_year: int

    @classmethod
    def new(cls, id: int, title: str, director: str, release_year: int) -> "Movie":
        """Equivalent of `impl Movie { fn new(...) -> Self }`.

        A `@classmethod` receives the class itself as its first argument (`cls`),
        in the same way a regular method receives the instance (`self`).
        """
        return cls(id=id, title=title, director=director, release_year=release_year)
