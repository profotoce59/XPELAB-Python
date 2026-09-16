"""API tests, with the database mocked out.

`TestClient` calls the FastAPI app in-process: no server to start, no port
to bind. `monkeypatch` replaces the datasource functions so the tests run
without Postgres.
"""

import pytest
from fastapi.testclient import TestClient

from src.datasource import postgres_datasource
from src.main import create_app
from src.models import Movie


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    fake_db: dict[int, Movie] = {
        1: Movie.new(1, "Matrix", "Wachowski", 1999),
    }

    def fake_fetch_movies() -> list[Movie]:
        return list(fake_db.values())

    def fake_fetch_movie(movie_id: int) -> Movie:
        if movie_id not in fake_db:
            from src.errors import XpelabError

            raise XpelabError(f"Movie {movie_id} not found")
        return fake_db[movie_id]

    def fake_create_movie(movie: Movie) -> Movie:
        new_id = max(fake_db, default=0) + 1
        created = Movie.new(new_id, movie.title, movie.director, movie.release_year)
        fake_db[new_id] = created
        return created

    monkeypatch.setattr(postgres_datasource, "fetch_movies_from_db", fake_fetch_movies)
    monkeypatch.setattr(postgres_datasource, "fetch_movie_from_db", fake_fetch_movie)
    monkeypatch.setattr(postgres_datasource, "create_movie_in_db", fake_create_movie)

    return TestClient(create_app())


def test_get_movies(client: TestClient) -> None:
    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Matrix", "director": "Wachowski", "release_year": 1999}
    ]


def test_get_movie_by_id(client: TestClient) -> None:
    assert client.get("/movies/1").json()["title"] == "Matrix"
    assert client.get("/movies/42").status_code == 404


def test_create_movie(client: TestClient) -> None:
    response = client.post(
        "/movies",
        json={"title": "Inception", "director": "Nolan", "release_year": 2010},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 2


def test_validation_error(client: TestClient) -> None:
    """A missing field gives a 422 - FastAPI validated it for us."""
    response = client.post("/movies", json={"title": "Incomplete"})
    assert response.status_code == 422
