"""Error handling.

Rust returns errors: `Result<T, E>`, and the compiler makes you handle them.
Python raises them: an exception interrupts the flow and travels up the call
stack until something catches it. Nothing forces a caller to catch anything,
which is the main trade-off between the two languages.

Run: python -m src.examples.errors
"""


class XpelabError(Exception):
    """A custom exception - the equivalent of `struct XpelabError`.

    Inheriting from Exception is all it takes. Define your own so that
    callers can catch YOUR errors without catching everyone else's.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class MovieNotFoundError(XpelabError):
    """Exceptions form a hierarchy: catching XpelabError catches this too."""


def divide(a: float, b: float) -> float:
    """Raises instead of returning `Err(...)`."""
    if b == 0.0:
        raise XpelabError("Division by zero")
    return a / b


def find_movie(movies: dict[int, str], movie_id: int) -> str:
    if movie_id not in movies:
        raise MovieNotFoundError(f"Movie {movie_id} not found")
    return movies[movie_id]


def load_config(path: str) -> str:
    """`raise ... from error` is the closest thing to the `?` operator.

    It re-raises as your own error type while keeping the original cause
    visible in the traceback.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as error:
        raise XpelabError(f"Cannot read {path}") from error


def main() -> None:
    # try / except / else / finally
    try:
        print(f"10 / 2 = {divide(10, 2)}")
        print(f"10 / 0 = {divide(10, 0)}")
    except XpelabError as error:
        # `as error` binds the exception object.
        print(f"Caught: {error}")
    else:
        # Runs only if NO exception was raised.
        print("No error")
    finally:
        # Always runs - the cleanup slot.
        print("Done with division")

    movies = {1: "Matrix", 2: "Inception"}
    for movie_id in (1, 42):
        try:
            print(f"Movie {movie_id}: {find_movie(movies, movie_id)}")
        except MovieNotFoundError as error:
            print(f"Not found: {error}")

    # Catching several types, and catching the parent type.
    try:
        find_movie(movies, 99)
    except (ValueError, XpelabError) as error:
        print(f"Caught via the parent class: {type(error).__name__}: {error}")

    try:
        load_config("/does/not/exist.toml")
    except XpelabError as error:
        print(f"{error}  (caused by: {type(error.__cause__).__name__})")

    # The equivalent of `panic!`: an uncaught exception stops the program.
    # Never write a bare `except:` - it swallows everything, including
    # Ctrl+C and programming mistakes you wanted to see.
    print("\nUncaught exceptions terminate the program, like panic!()")


if __name__ == "__main__":
    main()
