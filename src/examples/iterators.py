"""Iterators and generators.

Rust has lazy iterators (`.iter().map().filter()`), and so does Python -
but Python gives you a dedicated syntax for building them: `yield`.

Run: python -m src.examples.iterators
"""

from collections.abc import Iterator


def countdown(start: int) -> Iterator[int]:
    """A generator function.

    The presence of `yield` changes everything: calling this function does
    NOT run the body, it returns a generator. The body advances one `yield`
    at a time, each time the caller asks for the next value.
    """
    current = start
    while current > 0:
        yield current
        current -= 1


def read_large_file_lines(lines: list[str]) -> Iterator[str]:
    """Why it matters: nothing is ever held in memory at once.

    You can iterate over a 10 GB file, or an infinite sequence, without
    allocating anything.
    """
    for line in lines:
        stripped = line.strip()
        if stripped:
            yield stripped


class Fibonacci:
    """An iterator written by hand.

    Implementing `__iter__` and `__next__` is what makes an object usable
    in a `for` loop. It is the equivalent of implementing Rust's `Iterator`.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.a, self.b = 0, 1
        self.count = 0

    def __iter__(self) -> "Fibonacci":
        return self

    def __next__(self) -> int:
        if self.count >= self.limit:
            # Raising StopIteration is how an iterator says "I am done".
            # The `for` loop catches it for you.
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value


def main() -> None:
    print(f"countdown(5): {list(countdown(5))}")

    # A generator is lazy: it produces values on demand.
    generator = countdown(3)
    print(f"The generator object itself: {generator}")
    print(f"next(): {next(generator)}, {next(generator)}, {next(generator)}")

    lines = ["  first  ", "", "second", "   ", "third"]
    print(f"Cleaned lines: {list(read_large_file_lines(lines))}")

    print(f"Fibonacci: {list(Fibonacci(10))}")

    # A generator EXPRESSION: like a comprehension, with () instead of [].
    # Nothing is built in memory.
    squares = (x * x for x in range(1_000_000))
    print(f"First 5 squares, out of a million: {[next(squares) for _ in range(5)]}")

    # The itertools module is Python's standard iterator toolbox.
    import itertools

    print(f"take(5) on an infinite counter: {list(itertools.islice(itertools.count(10), 5))}")
    print(f"chain: {list(itertools.chain([1, 2], [3, 4]))}")

    # Builtins that consume an iterator
    numbers = [4, 8, 15, 16, 23, 42]
    print(f"sum={sum(numbers)}, min={min(numbers)}, max={max(numbers)}")
    print(f"any(>40)={any(n > 40 for n in numbers)}, all(>0)={all(n > 0 for n in numbers)}")


if __name__ == "__main__":
    main()
