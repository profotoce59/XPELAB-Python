"""Protocols and abstract base classes - the equivalent of traits.

Rust defines shared behaviour with a `trait` and `impl Trait for Type`.
Python has two ways of doing this:

1. ABC (abstract base class): explicit inheritance. The class says
   "I implement this interface". Closest to a Java interface.

2. Protocol: structural typing, a.k.a. duck typing that the type checker
   understands. Any class with the right methods satisfies the protocol,
   without inheriting from anything - which is much closer to how a Rust
   trait can be implemented for a type you do not own.

Run: python -m src.examples.06_protocols
"""

from abc import ABC, abstractmethod
from typing import Protocol


# --- Approach 1: ABC -------------------------------------------------------
class Greeter(ABC):
    @abstractmethod
    def greet(self) -> str:
        """Subclasses MUST implement this; instantiating Greeter fails."""

    def greet_loudly(self) -> str:
        """An ABC can also provide a default implementation.

        This is the equivalent of a default method on a Rust trait.
        """
        return self.greet().upper()


class Person(Greeter):
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self) -> str:
        return f"Hello, my name is {self.name}."


# --- Approach 2: Protocol --------------------------------------------------
class Describable(Protocol):
    def describe(self) -> str: ...


class Movie:
    """Note: no inheritance. Having `describe()` is enough."""

    def __init__(self, title: str, year: int) -> None:
        self.title = title
        self.year = year

    def describe(self) -> str:
        return f"{self.title}, released in {self.year}"


class Actor:
    def __init__(self, name: str) -> None:
        self.name = name

    def describe(self) -> str:
        return f"the actor {self.name}"


def print_description(item: Describable) -> None:
    """Accepts anything that has a `describe()` method.

    Rust would write `fn print_description(item: &impl Describable)`.
    """
    print(f"  -> {item.describe()}")


def main() -> None:
    person = Person("Alice")
    print(person.greet())
    print(person.greet_loudly())

    try:
        Greeter()  # type: ignore[abstract]
    except TypeError as error:
        print(f"Cannot instantiate an ABC: {error}")

    print("Descriptions:")
    for item in (Movie("Matrix", 1999), Actor("Keanu Reeves")):
        print_description(item)


if __name__ == "__main__":
    main()
