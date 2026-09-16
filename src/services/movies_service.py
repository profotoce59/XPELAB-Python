"""Business layer.

The Rust lab wraps every database call in a `thread::spawn(...)` because
the `postgres` crate is blocking and Axum handlers are async.

Python has exactly the same problem and exactly the same answer: `psycopg`
used this way is blocking, so calling it directly inside an `async def`
handler would freeze the whole event loop. `asyncio.to_thread` runs the
blocking function in a worker thread and lets the loop keep serving other
requests meanwhile.
"""

import asyncio

from src.datasource import postgres_datasource as datasource
from src.models import Movie


async def create_movie(movie: Movie) -> Movie:
    return await asyncio.to_thread(datasource.create_movie_in_db, movie)


async def fetch_movies() -> list[Movie]:
    return await asyncio.to_thread(datasource.fetch_movies_from_db)


async def fetch_movie(movie_id: int) -> Movie:
    return await asyncio.to_thread(datasource.fetch_movie_from_db, movie_id)


async def update_movie(movie: Movie) -> Movie:
    return await asyncio.to_thread(datasource.update_movie_in_db, movie)
