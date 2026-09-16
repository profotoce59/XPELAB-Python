"""Variables, types and data structures.

Run: python -m src.examples.variables
"""

from enum import Enum


def main() -> None:
    # No keyword: assignment declares the variable.
    age = 30
    name = "Alice"
    print(f"Name: {name}, Age: {age}")

    # Every variable is mutable. There is no `mut`.
    score = 100
    print(f"Initial Score: {score}")
    score += 50
    print(f"Updated Score: {score}")

    can_vote = age >= 18
    print(f"Can Vote: {can_vote}")

    # Type hints are optional and NOT enforced at runtime. They document the
    # code and let tools (mypy, your IDE) catch mistakes before you run it.
    # This is the closest thing Python has to the Rust compiler.
    pi: float = 3.14
    is_active: bool = True
    print(f"pi={pi}, is_active={is_active}")

    # A "constant" is a convention, not a language feature: UPPER_CASE tells
    # readers not to reassign it. Nothing stops you from doing it anyway.
    MAX_RETRIES = 3
    print(f"MAX_RETRIES: {MAX_RETRIES}")

    # Enums
    class Color(Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    favorite_color = Color.GREEN
    print(f"My favorite color is {favorite_color} (value: {favorite_color.value})")

    # Tuple: immutable, fixed size, can mix types.
    person: tuple[str, int, bool] = ("Alice", 30, True)
    person_name, person_age, person_active = person  # unpacking
    print(f"Tuple values: {person_name}, {person_age}, {person_active}")

    # List: mutable, growable. The everyday Python collection.
    # It CAN hold different types, but a list is meant to be traversed
    # uniformly: `sum([1, "two"])` raises a TypeError. Keep a list
    # homogeneous in behaviour; for a record whose positions mean
    # different things, use a tuple or a dataclass.
    numbers: list[int] = [1, 2, 3, 4, 5]
    numbers.append(6)
    print(f"List: {numbers}")

    # Dict: key -> value. There is no equivalent in the Rust lab, but it is
    # everywhere in Python (a JSON body, an object's attributes, kwargs...).
    movie: dict[str, object] = {"title": "Matrix", "year": 1999}
    print(f"Dict: {movie}, title = {movie['title']}")

    # Set: unordered, no duplicates.
    tags: set[str] = {"action", "sci-fi", "action"}
    print(f"Set: {tags}")

    # Strings. Python has a single string type, `str`, always UTF-8 text.
    # No `&str` / `String` distinction: the ownership problem it solves
    # does not exist here.
    text = "Hello, Python!"
    print(f"Upper: {text.upper()}, length: {len(text)}")

    # Slices: [start:stop:step], stop is EXCLUDED (like Rust's `..`).
    print(f"numbers[1:4] = {numbers[1:4]}")   # elements 1, 2, 3
    print(f"numbers[:3]  = {numbers[:3]}")    # from the start
    print(f"numbers[2:]  = {numbers[2:]}")    # to the end
    print(f"numbers[:]   = {numbers[:]}")     # a full copy
    print(f"numbers[::2] = {numbers[::2]}")   # every other element
    print(f"numbers[-1]  = {numbers[-1]}")    # negative index: from the end
    print(f"text[:5]     = {text[:5]}")       # slicing works on strings too

    # None is the absence of a value: Rust's `None`, but without `Option<T>`
    # wrapping it. A function that "returns nothing" returns None.
    maybe_director: str | None = None
    print(f"Director: {maybe_director if maybe_director is not None else 'unknown'}")


if __name__ == "__main__":
    main()
