"""Closures, lambdas and functions as values.

In Python a function is an ordinary object: you can put it in a variable,
pass it as an argument, return it from another function.

Run: python -m src.examples.09_closures
"""

from collections.abc import Callable


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Returns a closure that captured `factor`.

    Rust would ask you to think about whether `factor` is moved or
    borrowed. Python just keeps a reference alive as long as the
    inner function exists.
    """

    def multiply(value: int) -> int:
        return value * factor

    return multiply


def make_counter() -> Callable[[], int]:
    """`nonlocal` lets the closure REASSIGN a captured variable.

    Without it, `count += 1` would create a new local variable
    (same rule as `global` in functions.py).
    """
    count = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


def main() -> None:
    # lambda: a one-expression anonymous function.
    # Rust: let add = |a, b| a + b;
    add = lambda a, b: a + b  # noqa: E731
    print(f"add(5, 3) = {add(5, 3)}")
    # Style note: PEP 8 says prefer `def` over assigning a lambda to a name.
    # Lambdas are meant to be passed inline, as below.

    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(21) = {double(21)}, triple(7) = {triple(7)}")

    counter = make_counter()
    print(f"counter: {counter()}, {counter()}, {counter()}")

    movies = [("Matrix", 1999), ("Inception", 2010), ("Alien", 1979)]

    # Functions taking functions: sorted, map, filter.
    print(f"By year: {sorted(movies, key=lambda movie: movie[1])}")
    print(f"By title: {sorted(movies, key=lambda movie: movie[0])}")

    titles = list(map(lambda movie: movie[0], movies))
    print(f"map:    {titles}")

    recent = list(filter(lambda movie: movie[1] > 1990, movies))
    print(f"filter: {recent}")

    # In practice a comprehension is more Pythonic than map/filter:
    print(f"comprehension: {[m[0] for m in movies if m[1] > 1990]}")


if __name__ == "__main__":
    main()
