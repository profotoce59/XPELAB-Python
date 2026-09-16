"""References, mutability and copies - the counterpart to Rust's ownership.

This is the chapter where Python and Rust differ the most.

Rust: one value, one owner. Assignment MOVES the value, and the compiler
refuses to let you use the old name afterwards.

Python: a variable is a NAME pointing at an object. Assignment copies the
pointer, never the object. Two names can point at the same object, and
memory is reclaimed by the garbage collector once nobody points at it
anymore. Nothing is checked at compile time - which is why the bugs Rust
prevents at compile time are bugs you hit at runtime in Python.

Run: python -m src.examples.04_mutability
"""

import copy


def main() -> None:
    # The Rust example: `let s2 = s1;` invalidates s1.
    s1 = "Hello, Python!"
    s2 = s1
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print("Both are still valid: Python moved nothing, it copied a reference.\n")

    # `id()` returns the object's address: proof that both names point
    # at the same object.
    print(f"id(s1) == id(s2): {id(s1) == id(s2)}\n")

    # This matters as soon as the object is MUTABLE.
    original = [1, 2, 3]
    alias = original          # NOT a copy: the same list, under two names
    alias.append(4)
    print(f"original: {original}   <- modified through `alias`")
    print(f"alias:    {alias}\n")

    # To get a real copy, ask for one.
    shallow = original.copy()      # or list(original), or original[:]
    shallow.append(5)
    print(f"original after shallow copy + append: {original}")
    print(f"shallow:                             {shallow}\n")

    # A shallow copy only copies the outer container. Nested objects
    # are still shared.
    nested = [[1, 2], [3, 4]]
    shallow_nested = nested.copy()
    shallow_nested[0].append(99)
    print(f"nested:         {nested}   <- the inner list was shared!")
    deep_nested = copy.deepcopy(nested)
    deep_nested[0].append(100)
    print(f"nested:         {nested}   <- deepcopy left it alone")
    print(f"deep_nested:    {deep_nested}\n")

    # Mutable vs immutable types
    #   immutable: int, float, str, bool, tuple, frozenset, None
    #   mutable  : list, dict, set, and most of your own classes
    # "Modifying" an immutable object actually creates a new one.
    text = "abc"
    print(f"id before: {id(text)}")
    text += "d"
    print(f"id after:  {id(text)}  <- a different object\n")

    # Which is why passing an argument behaves differently depending on
    # the type. Python always passes the reference; whether the caller
    # sees a change depends on whether the object can be mutated.
    def try_to_modify(number: int, items: list[int]) -> None:
        number += 100        # rebinds a local name, the caller sees nothing
        items.append(100)    # mutates the shared object, the caller sees it

    n = 1
    lst = [1]
    try_to_modify(n, lst)
    print(f"n after the call:   {n}    <- unchanged (int is immutable)")
    print(f"lst after the call: {lst}  <- changed (list is mutable)")


if __name__ == "__main__":
    main()
