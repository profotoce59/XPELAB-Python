"""HTTP handlers.

Like in the Rust lab, handlers are plain functions: they know nothing about
routing (that lives in `src/routes`) and nothing about SQL (that lives in
`src/datasource`). They translate between HTTP and the business layer.

FastAPI reads the type hints to do its job:
  - `movie: Movie` (a pydantic model) => parse and validate the JSON body
  - `movie_id: int` (declared in the path) => parse and validate the path parameter
  - `-> Movie` => serialize the response to JSON
This is what `Json<Movie>` and `Path<u32>` do in Axum, except the annotation
is the ordinary Python type hint.
"""

from fastapi import HTTPException

from src.errors import XpelabError
from src.models import Movie
from src.services import movies_service


async def create_movie(movie: Movie) -> Movie:
    try:
        return await movies_service.create_movie(movie)
    except XpelabError as error:
        # Raising HTTPException is how FastAPI returns an error status code.
        raise HTTPException(status_code=500, detail=error.message) from error


async def get_movies() -> list[Movie]:
    try:
        return await movies_service.fetch_movies()
    except XpelabError as error:
        raise HTTPException(status_code=500, detail=error.message) from error


async def get_movie_by_id(movie_id: int) -> Movie:
    try:
        return await movies_service.fetch_movie(movie_id)
    except XpelabError as error:
        raise HTTPException(status_code=404, detail=error.message) from error


async def update_movie(movie: Movie) -> Movie:
    try:
        return await movies_service.update_movie(movie)
    except XpelabError as error:
        raise HTTPException(status_code=500, detail=error.message) from error
