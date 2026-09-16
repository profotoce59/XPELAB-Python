"""Modules and imports.

Rust has three ways of declaring a module (inline, file, directory) and
requires `mod` to wire them together. Python has one rule: every .py file
IS a module, every directory containing __init__.py IS a package. Nothing
needs declaring, only importing.

Run: python -m src.examples.11_modules
"""

# 1. Import a whole module - the name stays qualified.
import math

# 2. Import specific names into the current scope.
from datetime import datetime

# 3. Rename on import, to avoid a clash or shorten a long name.
from collections import OrderedDict as Ordered

# 4. Import from our own package. This path is ABSOLUTE, starting from the
#    project root: it works because we run `python -m src.examples.11_modules`
#    from the root, so the root is on sys.path.
from src.errors import XpelabError

# `from x import *` exists. Do not use it: it hides where names come from
# and silently overwrites existing ones.


# An inline "module" is done with a class or, more often, a nested function.
# Python has no `mod { ... }` block.
def _helper(a: int, b: int) -> int:
    """A leading underscore is the convention for "private".

    It is a convention only - nothing prevents another module from
    importing it. Python has no `pub`.
    """
    return a + b


def main() -> None:
    print(f"math.pi = {math.pi:.5f}, math.sqrt(16) = {math.sqrt(16)}")
    print(f"Now: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Renamed import: {Ordered([('a', 1), ('b', 2)])}")
    print(f"From our own package: {XpelabError('example').message}")
    print(f"Private helper: {_helper(5, 3)}")

    print(f"\nThis module's name: {__name__}")
    print("When imported it would be 'src.examples.11_modules' instead.")

    # A few standard library modules worth knowing:
    #   pathlib   - file paths, use it instead of os.path
    #   json      - serialization (serde_json)
    #   typing    - type hints
    #   dataclasses, enum, collections, itertools, functools
    #   datetime, logging, argparse, unittest, asyncio
    import pathlib

    here = pathlib.Path(__file__)
    print(f"\nThis file: {here.name}, in {here.parent.name}/")


if __name__ == "__main__":
    main()
