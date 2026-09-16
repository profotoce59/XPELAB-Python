"""Route declarations.

Rust:

    Router::new()
        .route("/movies", post(create_movie))
        .route("/movies", get(get_movies))

FastAPI is usually written with decorators (`@app.get("/movies")`) directly
on top of the handler. We use `add_api_route` here to keep the same shape as
the Rust lab: handlers on one side, the routing table on the other.

The `{movie_id}` in the path must match the name of the handler parameter.
"""

from fastapi import APIRouter

from src.handlers.movies_handler import (
    create_movie,
    get_movie_by_id,
    get_movies,
    update_movie,
)


def create_router() -> APIRouter:
    router = APIRouter()
    router.add_api_route("/movies", create_movie, methods=["POST"])
    router.add_api_route("/movies", get_movies, methods=["GET"])
    router.add_api_route("/movies/{movie_id}", get_movie_by_id, methods=["GET"])
    router.add_api_route("/movies", update_movie, methods=["PUT"])
    return router
