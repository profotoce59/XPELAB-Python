"""Functions: parameters, return values, None, scopes.

Run: python -m src.examples.03_functions
"""


def greet(name: str) -> None:
    """`-> None` means the function returns nothing useful."""
    print(f"Hello, {name}!")


def add(a: int, b: int) -> int:
    """Unlike Rust, the `return` keyword is mandatory.

    A function without an explicit `return` returns None.
    """
    return a + b


def divide(numerator: float, denominator: float) -> float | None:
    """The Python answer to `Option<f64>`.

    There is no `Some(...)` wrapper: you return the value, or None.
    The price is that the caller must remember to check, and the type
    checker is the only thing reminding them.
    """
    if denominator == 0.0:
        return None
    return numerator / denominator


def describe_movie(title: str, year: int = 2026, *actors: str, **details: str) -> str:
    """Python parameters are much more flexible than Rust's.

    - `year=2026`      : default value (Rust has no such thing)
    - `*actors`        : any number of extra positional arguments (a tuple)
    - `**details`      : any number of named arguments (a dict)
    """
    parts = [f"{title} ({year})"]
    if actors:
        parts.append(f"starring {', '.join(actors)}")
    for key, value in details.items():
        parts.append(f"{key}={value}")
    return " | ".join(parts)



def main() -> None:
    greet("Alice")
    print(f"Sum: {add(5, 10)}")

    result = divide(10.0, 2.0)
    if result is not None:
        print(f"Division Result: {result}")
    else:
        print("Cannot divide by zero")

    print(describe_movie("Matrix"))
    print(describe_movie("Matrix", 1999, "Keanu Reeves", "Carrie-Anne Moss", genre="sci-fi"))


if __name__ == "__main__":
    main()
