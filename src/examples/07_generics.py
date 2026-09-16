"""Generics.

Rust:
    fn highest_value<T: PartialOrd + Copy>(values: &[T]) -> Option<T>

Python has generics too, but they are a TYPE CHECKER feature only. At
runtime the interpreter erases them entirely: it never checks that T is
comparable, it just tries `>` and raises a TypeError if that fails.

Run: python -m src.examples.07_generics
"""

from typing import Generic, Protocol, TypeVar


class Comparable(Protocol):
    """The equivalent of the `PartialOrd` bound."""

    def __gt__(self, other: object, /) -> bool: ...


# A TypeVar is a placeholder for "some type, the same one throughout".
# `bound=` is the equivalent of a Rust trait bound.
T = TypeVar("T", bound=Comparable)


def highest_value(values: list[T]) -> T | None:
    if not values:  # an empty list is falsy
        return None
    highest = values[0]
    for value in values:
        if value > highest:
            highest = value
    return highest


# Generic classes: the equivalent of `struct Stack<T>`.
I = TypeVar("I")


class Stack(Generic[I]):
    def __init__(self) -> None:
        self._items: list[I] = []

    def push(self, item: I) -> None:
        self._items.append(item)

    def pop(self) -> I | None:
        return self._items.pop() if self._items else None

    def __len__(self) -> int:
        """Implementing `__len__` makes `len(stack)` work.

        Python's "traits" are mostly these dunder methods.
        """
        return len(self._items)


def main() -> None:
    int_values = [10, 20, 5, 30, 15]
    highest_int = highest_value(int_values)
    if highest_int is not None:
        print(f"Highest integer value: {highest_int}")
    else:
        print("The integer list is empty.")

    float_values = [10.5, 20.3, 5.7, 30.1, 15.6]
    print(f"Highest float value: {highest_value(float_values)}")

    # It also works on strings: `str` supports `>`. The function was never
    # told about strings - and never had to be.
    print(f"Highest string value: {highest_value(['Neo', 'Trinity', 'Morpheus'])}")

    print(f"Empty list: {highest_value([])}")

    # There is no turbofish in Python: no type is passed at runtime, so
    # there is nothing to disambiguate. If you need to help the type
    # checker, you annotate the variable instead:
    #     result: int | None = highest_value(int_values)

    stack: Stack[str] = Stack()
    stack.push("first")
    stack.push("second")
    print(f"Stack length: {len(stack)}, popped: {stack.pop()}")

    # Python 3.12+ offers a lighter syntax (PEP 695), with no TypeVar
    # declaration, which is much closer to Rust:
    #     def highest_value[T: Comparable](values: list[T]) -> T | None: ...
    #     class Stack[I]: ...


if __name__ == "__main__":
    main()
