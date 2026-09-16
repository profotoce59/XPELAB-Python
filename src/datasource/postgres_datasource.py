"""Database access, raw SQL.

Same choice as the Rust lab: no ORM, the queries are written by hand.
`psycopg` is the PostgreSQL driver for Python (version 3).

Note the `%s` placeholders: psycopg uses them where Rust used `$1`, `$2`.
NEVER build a query with an f-string or string concatenation, that is how
SQL injections happen. The driver escapes the parameters for you.
"""

import os

import psycopg

from src.errors import XpelabError
from src.models import Movie


def connect_to_db() -> psycopg.Connection:
    """Open a connection to the database.

    `os.environ["..."]` raises a KeyError if the variable is missing,
    which is the equivalent of Rust's `.expect("DATABASE_URL must be set")`.
    """
    database_url = os.environ.get("DATABASE_URL")
    if database_url is None:
        raise XpelabError("DATABASE_URL must be set")
    return psycopg.connect(database_url)


def initialize_db() -> None:
    """Create the `movies` table if it does not exist yet."""
    try:
        # `with` is a context manager: it guarantees the connection gets
        # closed, even if an exception is raised. It is the Python answer to
        # Rust's `Drop` trait.
        with connect_to_db() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS movies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    director VARCHAR NOT NULL,
                    year INT NOT NULL
                )
                """
            )
    except psycopg.Error as error:
        # `raise ... from error` keeps the original error in the traceback.
        raise XpelabError(f"Database initialization error: {error}") from error


def create_movie_in_db(movie: Movie) -> Movie:
    """Insert a movie and return it with the id assigned by Postgres."""
    try:
        with connect_to_db() as connection:
            row = connection.execute(
                "INSERT INTO movies (title, director, year) VALUES (%s, %s, %s) RETURNING id",
                (movie.title, movie.director, movie.release_year),
            ).fetchone()
    except psycopg.Error as error:
        raise XpelabError(f"Database query error: {error}") from error

    if row is None:
        raise XpelabError("Insert did not return an id")

    return Movie.new(row[0], movie.title, movie.director, movie.release_year)


def fetch_movies_from_db() -> list[Movie]:
    """Return every movie in the table."""
    try:
        with connect_to_db() as connection:
            rows = connection.execute(
                "SELECT id, title, director, year FROM movies"
            ).fetchall()
    except psycopg.Error as error:
        raise XpelabError(f"Database query error: {error}") from error

    # List comprehension: the idiomatic Python way to transform a collection.
    # Rust would write `.iter().map(...).collect()`.
    return [Movie.new(row[0], row[1], row[2], row[3]) for row in rows]


def fetch_movie_from_db(movie_id: int) -> Movie:
    """Return a single movie, or raise if it does not exist."""
    try:
        with connect_to_db() as connection:
            row = connection.execute(
                "SELECT id, title, director, year FROM movies WHERE id = %s",
                (movie_id,),
            ).fetchone()
    except psycopg.Error as error:
        raise XpelabError(f"Database query error: {error}") from error

    if row is None:
        raise XpelabError(f"Movie {movie_id} not found")

    return Movie.new(row[0], row[1], row[2], row[3])


def update_movie_in_db(movie: Movie) -> Movie:
    """Update a movie and return the stored version."""
    if movie.id is None:
        raise XpelabError("Movie ID is required for update")

    try:
        with connect_to_db() as connection:
            connection.execute(
                "UPDATE movies SET title = %s, director = %s, year = %s WHERE id = %s",
                (movie.title, movie.director, movie.release_year, movie.id),
            )
    except psycopg.Error as error:
        raise XpelabError(f"Database query error: {error}") from error

    return fetch_movie_from_db(movie.id)
