# XPELAB PYTHON

This project was created to be used as a learning support for those who want to try Python.

It is built around runnable code: every chapter below has a matching file under
`src/examples/` that you can execute, read and break. The last chapter puts it
all together into a small REST API backed by PostgreSQL.

## Getting Started

### Installation

Python 3.10 or later is required (3.12+ recommended). Check what you have:

```sh
python3 --version
```

- **macOS**: `brew install python@3.13`, or [python.org](https://www.python.org/downloads/)
- **Linux**: already there, otherwise `apt install python3 python3-venv`
- **Windows**: [python.org](https://www.python.org/downloads/) or `winget install Python.Python.3.13`

If you end up needing several Python versions side by side, look at
[pyenv](https://github.com/pyenv/pyenv) or [uv](https://docs.astral.sh/uv/).

### IDE Setup

Visual Studio Code with these two extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (includes Pylance, the type checker / language server)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) (linter and formatter)

PyCharm works out of the box if you prefer a full IDE.

### Project setup

Python isolates a project's dependencies in a **virtual environment**: a folder
holding its own copy of the interpreter and its own installed packages.

```sh
cd "xpelab python"

# Create the environment (the folder is git-ignored)
python3 -m venv .venv

# Activate it - macOS / Linux
source .venv/bin/activate
# Activate it - Windows PowerShell
.venv\Scripts\Activate.ps1

# Install the dependencies
pip install -r requirements.txt
```

Your prompt now starts with `(.venv)`. Everything you `pip install` lands in
that folder and nowhere else. `deactivate` gets you out.

**Why this matters:** without a venv, `pip install` writes into the system
Python, and two projects needing two different versions of the same library will
fight over it. Creating one is a manual step, and skipping it is the single most
common way to end up with a broken Python install.

### Running the examples

Each file under `src/examples/` is a standalone, runnable lesson.

```sh
python -m src.examples.01_variables
python -m src.examples.02_control_flow
python -m src.examples.03_functions
python -m src.examples.04_mutability
python -m src.examples.05_classes
python -m src.examples.06_protocols
python -m src.examples.07_generics
python -m src.examples.08_errors
python -m src.examples.09_closures
python -m src.examples.10_iterators
python -m src.examples.11_modules
```

> Use `python -m src.examples.x`, not `python src/examples/x.py`. The `-m` form
> puts the project root on the import path, so `from src.models import Movie`
> resolves. This trips up everyone at least once.

## Variables

> `python -m src.examples.01_variables`

### Let's declare

There is no keyword. Assignment creates the variable.

```python
age = 39
pi = 3.14
name = "XPELAB"
is_active = True
```

### Types

Python is **dynamically typed**: the type belongs to the value, not to the
variable, and it is checked when the code runs.

Type hints let you write the type down anyway:

```python
age: int = 39
pi: float = 3.14
name: str = "XPELAB"
is_active: bool = True
```

**They are not enforced at runtime.** This runs without complaining:

```python
age: int = "not a number"   # works, Python does not care
```

Hints exist for your IDE, for the humans reading the code. Write
them on function signatures at the very least - that is where they pay off most.

There is one big exception: pydantic and FastAPI *read* the hints and validate
against them at runtime. That is exactly why we use them in the backend chapter.

### Constants

Python has none. The convention is `UPPER_CASE`, and it is only a convention -
nothing stops you from reassigning the name.

```python
MAX_RETRIES = 3     # please do not reassign this
```

### Enums

An `Enum` is a fixed set of named values. Use one instead of passing magic
strings around.

```python
from enum import Enum

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

direction = Direction.UP
print(direction.name, direction.value)   # UP up
```

When each case needs to carry *different* data, an `Enum` is the wrong tool.
Use one class per case and a union type:

```python
from dataclasses import dataclass

@dataclass
class Quit: ...

@dataclass
class Move:
    x: int
    y: int

@dataclass
class Write:
    text: str

Message = Quit | Move | Write

def handle(message: Message) -> None:
    match message:
        case Quit():
            print("quitting")
        case Move(x=x, y=y):
            print(f"moving to {x}, {y}")
        case Write(text=text):
            print(f"writing {text}")
        case _:
            raise ValueError(f"unknown message: {message}")
```

Note the `case _`: nothing checks that you covered every case, so the fallback
is on you.

### Sequences

| Type | Mutable | Notes |
| --- | --- | --- |
| `list` | yes | the default collection, ordered, growable |
| `tuple` | no | fixed size, often used to return several values |
| `dict` | yes | key -> value, keeps insertion order |
| `set` | yes | unordered, no duplicates |
| `str` | no | text, always Unicode |

```python
numbers: list[int] = [1, 2, 3, 4, 5]
names: tuple[str, ...] = ("Alice", "Bob", "Charlie")
ages: dict[str, int] = {"Alice": 30, "Bob": 25}
tags: set[str] = {"action", "sci-fi"}
```

A list is meant to be traversed **uniformly**: you write `for x in items:` or
`sum(items)` assuming every element responds the same way. Mixing types is
legal, but it breaks that assumption at runtime:

```python
values = [1, "two", 3.0]
sum(values)        # TypeError: unsupported operand type(s) for +: 'int' and 'str'
sorted(values)     # TypeError: '<' not supported between instances of 'str' and 'int'
```

The type is now `list[Any]`, so neither `mypy` nor your IDE can warn you - you
find out in production, and the only way to process the list becomes an
`isinstance` check inside the loop.

### Slices

`[start:stop:step]`, and `stop` is **excluded**.

```python
numbers = [1, 2, 3, 4, 5]

numbers[1:4]    # [2, 3, 4]
numbers[:3]     # [1, 2, 3]
numbers[2:]     # [3, 4, 5]
numbers[:]      # a full (shallow) copy
numbers[::2]    # [1, 3, 5]   every other element
numbers[::-1]   # [5, 4, 3, 2, 1]   reversed
numbers[-1]     # 5   negative indexes count from the end
```

Slicing works the same way on strings and tuples. Two things to know:

- A slice **builds a new object**, it is not a view onto the original. Slicing a
  large list inside a hot loop copies it every time.
- Slicing never raises for out-of-range bounds: `numbers[2:99]` is fine and
  returns what it can. Indexing does: `numbers[99]` raises `IndexError`.

### Tuples

```python
person: tuple[str, int, bool] = ("Alice", 30, True)
name, age, is_active = person        # unpacking

first, *rest = [1, 2, 3, 4]          # first=1, rest=[2, 3, 4]
```

Returning a tuple is the normal way to return several values:

```python
def min_max(values: list[int]) -> tuple[int, int]:
    return min(values), max(values)

lowest, highest = min_max([3, 1, 4])
```

## Control Flow

> `python -m src.examples.02_control_flow`

Blocks are defined by **indentation** (4 spaces), not braces. The colon opens the
block.

### If / Elif / Else

```python
number = 5
if number < 10:
    print("The number is less than 10")
elif number == 10:
    print("The number is equal to 10")
else:
    print("The number is greater than 10")
```

Anything can be tested for truth. Empty collections, `0`, `""` and `None` are
falsy:

```python
if not movies:            # instead of: if len(movies) == 0
    print("no movies")
```

Careful with that shortcut when `0` or `""` are legitimate values - `if not
count:` is also true when `count == 0`. Compare explicitly then:
`if count is None:`.

### While

```python
number = 3
while number != 0:
    print(f"{number}!")
    number -= 1
print("Liftoff!")
```

For an unconditional loop, write `while True:` and `break` out of it.

### For

`for` always iterates over a collection.

```python
for element in [10, 20, 30]:
    print(f"The value is: {element}")

for i in range(5):                  # 0, 1, 2, 3, 4
    print(i)

for index, value in enumerate(["a", "b"]):
    print(index, value)

for name, role in zip(names, roles):
    print(name, role)
```

`enumerate` and `zip` are the idiomatic answers to "I need the index too" and
"I need to walk two lists together". Reaching for `range(len(items))` is almost
always a sign one of them fits better.


### Match

Available from Python 3.10.

```python
number = 13
match number:
    case 1:
        print("One")
    case 2 | 3 | 5 | 7 | 11:
        print("This is a prime")
    case n if 13 <= n <= 19:        # a guard, for ranges
        print("A teen")
    case _:
        print("A number")
```

Its real strength is destructuring:

```python
match point:
    case (0, 0):        print("Origin")
    case (0, y):        print(f"On the Y axis at {y}")
```

**It is not exhaustive.** Forgetting a case is not an error - the `match` simply
does nothing and execution carries on. Always write a `case _`.

For a simple value-to-value mapping, a `dict` with `.get(key, default)` is
shorter and faster than a long `match`.

## References & Mutability

> `python -m src.examples.04_mutability`

This is the chapter that explains most surprising Python behaviour.

A variable is not a box holding a value. It is a **name bound to an object**.
Assignment binds a name to an object; it never copies the object. Several names
can therefore point at the same object, and memory is reclaimed automatically
once nothing points at it anymore.

```python
s1 = "hello"
s2 = s1          # s2 now points at the same string
```

Harmless with a string. Not harmless with a list:

```python
original = [1, 2, 3]
alias = original       # NOT a copy - the same list, under two names
alias.append(4)
print(original)        # [1, 2, 3, 4]
```

To actually copy:

```python
import copy

shallow = original.copy()        # or list(original), or original[:]
deep = copy.deepcopy(nested)     # also copies the nested objects
```

A shallow copy duplicates the outer container only. If the list contains other
lists, those are still shared - which is what `deepcopy` is for.

### Mutable vs immutable

- **Immutable**: `int`, `float`, `str`, `bool`, `tuple`, `frozenset`, `None`
- **Mutable**: `list`, `dict`, `set`, and most classes you write

"Modifying" an immutable object silently creates a new one - `text += "d"` binds
`text` to a brand new string, it does not edit the old one.

### What this means for function arguments

Arguments are passed the same way as any other binding. Whether the caller sees
a change depends on whether the object can be mutated at all:

```python
def modify(number: int, items: list[int]) -> None:
    number += 100      # rebinds a local name, caller sees nothing
    items.append(100)  # mutates the shared object, caller sees it
```

If a function is not supposed to modify what it receives, either copy it or
return a new object instead. Nothing enforces it for you, so say so in the name
and the docstring.

### The mutable default argument

The classic Python trap, and a direct consequence of the above:

```python
def bad(item, target=[]):        # evaluated ONCE, at definition time
    target.append(item)
    return target

bad("a")    # ['a']
bad("b")    # ['a', 'b']  <- the same list came back

def good(item, target=None):     # the correct pattern
    if target is None:
        target = []
    target.append(item)
    return target
```



### Comprehensions

The Python idiom for building a collection from another one.

```python
squares = [x * x for x in range(1, 6)]                       # list
even = [x for x in numbers if x % 2 == 0]                    # with a filter
by_length = {word: len(word) for word in words}              # dict
unique = {word.lower() for word in words}                    # set
lazy = (x * x for x in range(1_000_000))                     # generator, lazy
```

Readable up to one loop and one condition. 

## Functions

> `python -m src.examples.03_functions`

### Declaration

```python
def greet(name: str) -> None:
    print(f"Hello, {name}!")
```

`-> None` means the function returns nothing useful.

### Parameters & Return

`return` is mandatory. A function that falls off the end returns `None`.

```python
def add(a: int, b: int) -> int:
    return a + b
```

Parameters are flexible:

```python
def describe(title: str, year: int = 2026, *actors: str, **details: str) -> str:
    ...

describe("Matrix")                                  # default value
describe("Matrix", 1999, "Keanu", "Carrie-Anne")    # *args  -> a tuple
describe("Matrix", genre="sci-fi")                  # **kwargs -> a dict
```

- a parameter with a default must come after the ones without
- `*args` collects extra positional arguments into a tuple
- `**kwargs` collects extra named arguments into a dict
- remember: a **mutable** default is evaluated once and shared (see above)

There is **no function overloading**. Two `def` with the same name: the second
one silently replaces the first. Use default values or a union type instead.

### Docstrings

The string on the first line of a function is its documentation, reachable at
runtime through `help(function)` and `function.__doc__`, and shown by your IDE
on hover.

```python
def divide(a: float, b: float) -> float | None:
    """Return a / b, or None if b is zero."""
```

### The absence of a value

Python has no dedicated "maybe" wrapper. A function that may have nothing to
return returns `None`, and the type hint says so:

```python
def divide(a: float, b: float) -> float | None:
    if b == 0.0:
        return None
    return a / b

result = divide(10, 0)
if result is not None:          # use `is`, not `==`, to compare with None
    print(result)
```

Nothing forces the caller to check. Forget it and you get
`TypeError: unsupported operand` at runtime - which is precisely the class of
bug `mypy` exists to catch before you ship.

## Error Handling

> `python -m src.examples.08_errors`

Errors in Python are **raised**, not returned. A raised exception interrupts the
flow and travels up the call stack until something catches it. If nothing does,
the program stops and prints a traceback.

### Raising

```python
raise ValueError("Something went wrong!")
```

Pick the most specific built-in that fits (`ValueError`, `TypeError`,
`KeyError`, `FileNotFoundError`, ...) or define your own.

### Catching

```python
try:
    result = divide(10, 0)
except ZeroDivisionError as error:
    print(f"Caught: {error}")
except (ValueError, TypeError) as error:      # several types at once
    print(f"Other: {error}")
else:
    print("No exception was raised")          # only if nothing was raised
finally:
    print("Always runs")                      # cleanup
```

- Never write a bare `except:` - it swallows everything, including `Ctrl+C` and
  your own typos. Catch the exceptions you actually expect.

### Custom exceptions

```python
class XpelabError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class MovieNotFoundError(XpelabError):
    """Catching XpelabError catches this one too."""
```

Exceptions form a hierarchy, which lets a caller choose how specific it wants to
be. Give your application a base error class and inherit from it - callers can
then catch *your* errors without catching everyone else's.

### Re-raising with `from`

An exception you do not catch propagates on its own. When you want to convert a
low-level error into one of yours, `from` keeps the original cause visible in
the traceback:

```python
def load_config(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as error:
        raise XpelabError(f"Cannot read {path}") from error
```

Without `from`, the traceback loses the real reason and debugging gets much
harder.

### Context managers - `with`

`with` guarantees cleanup at the end of the block, whether it ends normally or
through an exception:

```python
with open("movies.json") as handle:     # closed automatically
    data = handle.read()

with connect_to_db() as connection:     # closed automatically
    connection.execute(...)
```

Any object implementing `__enter__` and `__exit__` works this way. Use it for
anything that must be released: files, sockets, database connections, locks.



## Closures

> `python -m src.examples.09_closures`

A function is an ordinary object: store it in a variable, pass it as an
argument, return it from another function.

```python
add = lambda a, b: a + b          # anonymous, one expression only
```

`lambda` is deliberately limited to a single expression - no statements, no
multiple lines. Style guides say not to assign one to a name (use `def` for
that); pass it inline instead:

```python
sorted(movies, key=lambda movie: movie.year)
list(map(lambda m: m.title, movies))
list(filter(lambda m: m.year > 1990, movies))
```

In practice, a comprehension usually reads better than `map`/`filter`:

```python
[m.title for m in movies if m.year > 1990]
```

A closure is a function that captured variables from the scope where it was
defined:

```python
def make_multiplier(factor: int):
    def multiply(value: int) -> int:
        return value * factor      # `factor` is captured
    return multiply

double = make_multiplier(2)
double(21)                         # 42
```

The captured variable stays alive as long as the closure does. To *reassign* it
from inside, use `nonlocal`:

```python
def make_counter():
    count = 0
    def increment() -> int:
        nonlocal count
        count += 1
        return count
    return increment
```

One trap: a closure captures the **variable**, not its value at capture time.
Building closures in a loop gives you several closures all seeing the loop
variable's final value. The fix is a default argument:
`lambda x, i=i: x + i`.

## Classes

> `python -m src.examples.05_classes`

A class groups data and the behaviour that goes with it.

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name            # attributes are created here
        self.age = age

    def greet(self) -> None:
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

person = Person("Alice", 30)        # no `new` keyword
person.greet()
```

`self` is **always** the first parameter of a method, and it is explicit -
Python passes the instance to the method, it does not hide it. `__init__` is not
a constructor that returns an object: Python creates the object first, then
calls `__init__` to configure it.

### Dataclasses

Three methods show up in nearly every class:

- `__init__` - builds the object. That is the one we just wrote by hand.
- `__repr__` - what you see when you print the object. Without it, Python shows
  `<Movie object at 0x104f2a3d0>`, which tells you nothing.
- `__eq__` - what `a == b` uses. Without it, two objects are equal only if they
  are literally the same object, so two identical movies compare as different.

Writing all three by hand gets old fast:

```python
from dataclasses import dataclass, field

@dataclass
class Movie:
    title: str
    year: int
    distribution: list[Distribution] = field(default_factory=list)
```

`@dataclass` generates all three from the annotations. Reach for it whenever a
class is mostly a bag of data. Options worth knowing: `@dataclass(frozen=True)`
makes instances immutable


### Dunder methods

Methods named `__like_this__` hook your class into the language itself. Defining
them is how your objects learn to behave like built-in ones:

| Method | Gives you |
| --- | --- |
| `__repr__` | `repr(obj)`, what the REPL and containers show - aim for unambiguous |
| `__str__` | `print(obj)`, `f"{obj}"` - aim for readable |
| `__eq__` | `a == b` |
| `__lt__`, `__gt__` | `a < b`, and sorting |
| `__len__` | `len(obj)`, and truthiness |
| `__iter__`, `__next__` | `for x in obj` |
| `__enter__`, `__exit__` | `with obj:` |
| `__call__` | `obj()` - the instance becomes callable |
| `__getitem__` | `obj[key]` |

If you define only one, make it `__repr__`. Debugging without it means reading
`<Movie object at 0x104f2a3d0>` all day.

### Properties, static and class methods

```python
class Movie:
    @property
    def age(self) -> int:
        return 2026 - self.year      # accessed as `movie.age`, no parentheses

    @staticmethod
    def is_classic(year: int) -> bool:
        return year < 1980           # no self, just namespaced in the class

    @classmethod
    def from_row(cls, row: tuple) -> "Movie":
        return cls(title=row[0], year=row[1])   # an alternative constructor
```

`@property` lets you turn an attribute into a computed value later without
changing any calling code. `@classmethod` receives the class itself, which makes
it the standard way to offer a second way of building an instance.

### Inheritance

```python
class Documentary(Movie):
    def __init__(self, title: str, year: int, subject: str) -> None:
        super().__init__(title=title, year=year)
        self.subject = subject
```

`super()` calls the parent implementation.

## Generics

> `python -m src.examples.07_generics`

Generics let one function or class work with several types while keeping the
relationship between its inputs and its output.

```python
from typing import TypeVar

T = TypeVar("T")

def highest_value(values: list[T]) -> T | None:
    if not values:
        return None
    highest = values[0]
    for value in values:
        if value > highest:
            highest = value
    return highest
```

Without `T`, the return type would be `object` and the caller would lose all
type information. With it, passing a `list[int]` gives back an `int | None`.

Constraints are written with `bound=`:

```python
class Comparable(Protocol):
    def __gt__(self, other: object, /) -> bool: ...

T = TypeVar("T", bound=Comparable)
```

Generic classes:

```python
from typing import Generic

I = TypeVar("I")

class Stack(Generic[I]):
    def __init__(self) -> None:
        self._items: list[I] = []
```

**Python 3.12+** offers a much lighter syntax (PEP 695), with no `TypeVar`
declaration:

```python
def highest_value[T: Comparable](values: list[T]) -> T | None: ...
class Stack[I]: ...
```

### Generics are erased at runtime

The interpreter ignores all of the above. There is one function, not one per
type, and **nothing checks the constraint when the code runs** - calling
`highest_value([{}, {}])` fails with a `TypeError` on `>`, not with a clear
error about the bound. Generics are a tool for the type checker and the reader;
run `mypy` if you want them to actually catch anything.

When the checker cannot infer the type on its own, annotate the variable:

```python
result: int | None = highest_value(numbers)
```

## Iterators & Generators

> `python -m src.examples.10_iterators`

This is one of the things Python does best.

```python
def countdown(start: int):
    current = start
    while current > 0:
        yield current           # `yield` makes this a generator
        current -= 1
```

The presence of `yield` changes the function completely: calling it runs
nothing, it returns a generator object. The body then advances one `yield` at a
time, each time the caller asks for the next value, and pauses in between
keeping all its local state.

The payoff is that nothing is ever fully in memory. You can iterate over a 10 GB
file, a database cursor, or an infinite sequence, with constant memory.

```python
lazy = (x * x for x in range(1_000_000))   # generator expression, nothing built
next(lazy)                                  # 0
```

To write an iterator by hand, implement `__iter__` and `__next__`:

```python
class Fibonacci:
    def __iter__(self): return self
    def __next__(self) -> int:
        if self.count >= self.limit:
            raise StopIteration          # how an iterator says "done"
        ...
```

`itertools` is the standard toolbox (`islice`, `chain`, `groupby`, `count`,
`cycle`), and `sum`, `min`, `max`, `any`, `all`, `sorted` consume any iterable.

One gotcha: a generator is **consumed once**. After you have iterated over it,
it is empty - there is no rewind. If you need the values twice, materialise them
with `list(...)`.

## Modules & Packages

> `python -m src.examples.11_modules`

The rules are short:

- every `.py` file **is** a module
- every directory with an `__init__.py` **is** a package
- `__init__.py` can stay empty - it just marks the folder as a package

Keep your code **out** of `__init__.py`. Put it in a file named after what it
contains, and use `__init__.py` only to re-export:

```python
# src/models/movie.py          <- the code lives here
class Movie(BaseModel): ...

# src/models/__init__.py       <- only the re-export
from src.models.movie import Movie

__all__ = ["Movie"]
```

Callers still write `from src.models import Movie`, so nothing changes for
them. Two reasons to bother: `__init__.py` runs on *every* import of the
package, so heavy code there slows things down and invites circular imports;
and someone looking for the `Movie` model opens `movie.py`, not `__init__.py`.
`__all__` declares what the package exports.

Nothing has to be declared anywhere. If the file exists, it can be imported.

```python
import math                                     # qualified: math.sqrt(16)
from datetime import datetime                   # into the current scope
from collections import OrderedDict as Ordered  # renamed
from src.models import Movie                    # from our own package
```

`from x import *` exists. Do not use it: it hides where names come from and
silently overwrites what is already there.

There is no `public` / `private` distinction. A leading underscore (`_helper`)
is the convention for "internal to this module", and it is a convention only.

### `if __name__ == "__main__"`

```python
if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` when the file is run directly, and the module's name
when it is imported. Without the guard, importing a module would execute its
script body as a side effect - which is why every runnable file in this lab has
it.

The same file can therefore be imported as a library and run as a script; Python
draws no distinction between the two.

### Circular imports

If `a.py` imports `b.py` and `b.py` imports `a.py`, you get an `ImportError`
that looks like a missing name. It is almost always a design signal: the shared
piece belongs in a third module. Moving an import inside a function is a
last-resort workaround, not a fix.

## Dependencies - PyPI

[PyPI](https://pypi.org) is the public package index.

```sh
pip install fastapi              # install
pip install "fastapi>=0.115"     # with a version constraint
pip freeze > requirements.txt    # pin everything currently installed
pip install -r requirements.txt  # reinstall from the file
```

`requirements.txt` lists what the project needs. What it does **not** do is lock
transitive dependencies - `pip install -r` on two different days can give two
different sets of versions.

This lab sticks to `pip` + `venv` because they ship with Python and there is
nothing extra to install.

## Static checks

Python will not stop you from shipping a typo. These two tools will:

```sh
pip install mypy ruff

mypy src              # checks the type hints
ruff check src        # linting (bugs, dead code, bad practice)
ruff format src       # formatting
```

`mypy` catches the bugs that type hints are there to prevent: a `None` you
forgot to check, a wrong argument type, a function called with a missing
argument. `ruff` is a very fast linter and formatter that replaces most of the
older toolchain (flake8, isort, black).

Run both in CI. Without them, type hints are documentation and nothing more.

## Tests

> `pytest`

Tests live in a `tests/` directory. Two naming conventions do the registration:
files named `test_*.py`, functions named `test_*`. There is nothing to declare.

```python
def test_add() -> None:
    assert add(2, 3) == 5
```

`assert` is a plain statement - pytest rewrites it so that a failure shows both
sides of the comparison instead of just "assertion failed".

```python
import pytest

def test_raises() -> None:
    with pytest.raises(XpelabError, match="boom"):
        do_something()

@pytest.mark.parametrize(("a", "b", "expected"), [(1, 1, 2), (0, 0, 0)])
def test_add_parametrized(a, b, expected) -> None:
    assert add(a, b) == expected

@pytest.fixture
def sample_movie() -> Movie:            # reusable setup, injected by name
    return Movie.new(1, "Matrix", "Wachowski", 1999)

def test_with_fixture(sample_movie: Movie) -> None:
    assert sample_movie.title == "Matrix"
```

`parametrize` runs one test against several inputs. `fixture` factors out setup:
declare it once, then any test that names it as a parameter receives it.

Run them:

```sh
pytest                       # everything
pytest -v                    # one line per test
pytest tests/test_api.py     # a single file
pytest -k "movie"            # tests whose name matches
pytest -x                    # stop at the first failure
```

The standard library also ships `unittest` (class-based). `pytest` is what
almost everyone actually uses.

## Go for a backend !

Let's create a simple REST API using the FastAPI framework and a PostgreSQL
database.

### Why FastAPI

FastAPI reads your **type hints** and does the work from them: it parses the
JSON body, validates it, converts path parameters, serializes the response, and
generates interactive API documentation. The annotations that are only
documentation everywhere else finally have teeth.

### Architecture

Each layer only knows the one below it, which is what makes any of them
replaceable or testable on its own:

```
src/
├── main.py                  # entry point, creates the app
├── routes/                  # the routing table: URL -> handler
│   └── movies_routes.py
├── handlers/                # HTTP in, HTTP out
│   └── movies_handler.py
├── services/                # business logic
│   └── movies_service.py
├── datasource/              # SQL
│   └── postgres_datasource.py
├── models/                  # pydantic models
│   └── movie.py
├── errors/                  # XpelabError
│   └── xpelab_error.py
└── examples/                # the runnable lessons
```

A handler knows nothing about SQL; the datasource knows nothing about HTTP. When
a bug appears, that tells you where to look.

### The model

```python
from pydantic import BaseModel

class Movie(BaseModel):
    id: int | None = None
    title: str
    director: str
    release_year: int
```

`BaseModel` validates at runtime. Send `"release_year": "yesterday"` and FastAPI
answers `422` with a precise error message, without you writing a line for it.
`id` is `int | None` because it does not exist yet at creation time.

### Raw SQL, no ORM

Queries are written by hand with `psycopg`, so that the SQL stays visible:

```python
row = connection.execute(
    "INSERT INTO movies (title, director, year) VALUES (%s, %s, %s) RETURNING id",
    (movie.title, movie.director, movie.release_year),
).fetchone()
```

Placeholders are `%s`, and the values go in a separate tuple. **Never build a
query with an f-string or string concatenation** - that is how SQL injection
happens. The driver escapes parameters for you.

### Blocking code in an async handler

FastAPI handlers are `async`, and `psycopg` used this way is blocking. Calling
it directly inside an `async def` would freeze the whole event loop and stall
every other request being served. The service layer moves it to a worker thread:

```python
import asyncio

async def fetch_movies() -> list[Movie]:
    return await asyncio.to_thread(datasource.fetch_movies_from_db)
```

This is the rule to remember about asyncio: **never call blocking code from a
coroutine**. File I/O, `time.sleep`, `requests`, a database driver - all of them
need `asyncio.to_thread` or an async-native library.

### Running it

**1. Start PostgreSQL.** With Docker:

```sh
docker run --name xpelab-postgres -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=xpelab -p 5432:5432 -d postgres:17
```

**2. Configure the environment.**

```sh
cp .env.example .env
```

```ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/xpelab
PORT=3000
```

`.env` is git-ignored: secrets never belong in the repository.

**3. Create the table:**

```sh
python -m src.examples.init_db
```

**4. Start the API:**

```sh
uvicorn src.main:app --reload --port 3000
```

`uvicorn` is the ASGI server that actually runs the app. `--reload` restarts it
on every file change.

**5. Call it:**

```sh
./curl_requests/create_movie.sh
./curl_requests/get_movies.sh
./curl_requests/update_movie.sh

curl http://localhost:3000/movies/1
```

**6. And the part you get for free** - interactive documentation, generated from
the type hints:

- <http://localhost:3000/docs> (Swagger UI, you can call the endpoints from there)
- <http://localhost:3000/redoc>
- <http://localhost:3000/openapi.json>

### Testing the API without a database

`tests/test_api.py` calls the app in-process with `TestClient` - no server to
start, no port to bind - and swaps the datasource functions out with
`monkeypatch`, so the tests run anywhere:

```sh
pytest tests/test_api.py -v
```

That is the payoff of the layering: because the handlers only talk to the
service layer, replacing what is underneath takes three lines.

## Gotchas recap

The things that bite everyone at least once:

| Gotcha | What to do |
| --- | --- |
| `def f(items=[])` - the default is shared across calls | use `None` and create the list inside |
| `b = a` does not copy a list | `a.copy()`, or `copy.deepcopy(a)` if nested |
| `if not count:` is true when `count == 0` | compare explicitly: `if count is None:` |
| `x == None` | always `x is None` |
| `match` without `case _` silently does nothing | always write the fallback |
| a bare `except:` swallows `Ctrl+C` and your typos | catch specific exceptions |
| `raise NewError(...)` loses the original cause | `raise NewError(...) from error` |
| a generator is empty after one pass | `list(...)` if you need it twice |
| modifying a list while iterating over it | build a new list |
| a decorator without `@functools.wraps` | breaks tracebacks and `help()` |
| type hints are not checked at runtime | run `mypy` |
| `pip install` outside a venv | activate the venv first |
| `python src/examples/x.py` fails on imports | `python -m src.examples.x` |
| blocking code inside `async def` | `await asyncio.to_thread(...)` |

## Data exercises - pandas & DuckDB

Three exercises on a real CSV: 7 668 films released between 1980 and 2020,
with their budget, box office, IMDb score, director and genre.

```sh
pip install -r requirements.txt     # adds pandas and duckdb
python -m src.exercises.download    # 1.3 MB into data/, git-ignored
```

```sh
python -m src.exercises.pandas_intro        # 1. load, clean, group
python -m src.exercises.duckdb_intro        # 2. the same questions, in SQL
python -m src.exercises.pandas_and_duckdb   # 3. both, on a question with a trap
```

**pandas** loads a file into memory as a `DataFrame` - a table with named
columns - and gives you a large vocabulary for reshaping it.

**DuckDB** is a database engine that runs inside your Python process, with no
server and no setup. It reads a CSV directly, so you can run SQL against a
file you never loaded.

They are not rivals: DuckDB can query a pandas DataFrame by variable name and
hand the result back as a DataFrame. Most real work uses both.

### 1. pandas

```python
import pandas as pd

movies = pd.read_csv("data/movies.csv")

movies.shape          # (7668, 15)
movies.head(3)        # look at it - never print a whole DataFrame
movies.dtypes         # what types pandas guessed
movies.isna().sum()   # where the holes are
```

Cheat Sheet : 
https://datascientyst.com/pandas-vs-sql-cheat-sheet/

`dtypes` is the one to check first. `object` means "a Python object", in
practice `str` - and a numeric column showing up as `object` tells you the
file contains something unexpected.

**Selecting rows** uses a boolean mask - a Series of True/False, one per row:

```python
movies[(movies["year"] >= 2010) & (movies["score"] >= 8)]
```

Use `&` `|` `~`, not `and` `or` `not`, and parenthesise each condition.
`and` raises `ValueError: The truth value of a Series is ambiguous`: it wants
one True or False, and a Series has 7 668 of them.

**Grouping** splits rows into groups, computes per group, glues back:

```python
directors = (
    movies.groupby("director")
    .agg(films=("name", "size"), avg_score=("score", "mean"))
    .reset_index()
)
directors[directors["films"] >= 5].sort_values("avg_score", ascending=False)
```

Prefer the named form `.agg(name=(column, function))` over
`.agg({"col": ["mean"]})`, which returns a MultiIndex you then have to
flatten. And call `.reset_index()`, or you will fight the index for the rest
of the script.

Filtering *after* aggregating is what stops one-hit wonders from winning.
The answer here is Christopher Nolan, then Hayao Miyazaki.

**Cleaning** is most of the work. `released` holds `"June 13, 1980 (United
States)"` - a date and a country in one field:

```python
parts = movies["released"].str.extract(r"^(?P<date>[^(]+?)\s*\((?P<country>[^)]+)\)$")
movies["release_date"] = pd.to_datetime(parts["date"], format="%B %d, %Y", errors="coerce")
```

`errors="coerce"` turns anything unparseable into `NaT` instead of raising and
losing the whole column. Pass `format=` when you know it: without it pandas
has to infer, which is slower and can silently swap day and month.

### 2. DuckDB

```python
import duckdb

duckdb.sql("SELECT COUNT(*) FROM 'data/movies.csv'").fetchone()
```

That is the whole setup. No server, no `CREATE TABLE`, no import step -
DuckDB reads the file itself.

```sql
SELECT director, COUNT(*) AS films, ROUND(AVG(score), 2) AS avg_score
FROM 'data/movies.csv'
WHERE score IS NOT NULL
GROUP BY director
HAVING COUNT(*) >= 5
ORDER BY avg_score DESC
LIMIT 5
```

Same answer as the pandas chain above, in one statement. `WHERE` filters rows
*before* grouping, `HAVING` filters groups *after* aggregating - which is why
`WHERE COUNT(*) >= 5` is a syntax error.

**Top N per group** is where SQL pulls ahead:

```sql
SELECT (year // 10) * 10 AS decade, genre, COUNT(*) AS films
FROM 'data/movies.csv'
GROUP BY 1, 2
QUALIFY ROW_NUMBER() OVER (PARTITION BY decade ORDER BY films DESC) = 1
```

`ROW_NUMBER() OVER (PARTITION BY decade ORDER BY ...)` numbers rows 1, 2,
3... restarting at each decade. `QUALIFY` filters on that number - `WHERE`
cannot, because the number does not exist yet at that stage. `QUALIFY` is to
window functions what `HAVING` is to `GROUP BY`.

> DuckDB also offers `SELECT * EXCLUDE (...)` and `GROUP BY ALL`. Both are
> DuckDB extensions, not standard SQL, and `GROUP BY ALL` cannot currently be
> combined with `QUALIFY`.

#### The trap: integer division differs between the two

```python
1986 // 10 * 10               # Python  -> 1980
```
```sql
(1986 / 10)::INT * 10         -- DuckDB  -> 1990   WRONG
(1986 // 10) * 10             -- DuckDB  -> 1980
FLOOR(1986 / 10) * 10         -- DuckDB  -> 1980
```

In DuckDB `/` is floating-point division and `::INT` **rounds to the
nearest** integer: 198.6 becomes 199. Python's `//` truncates.

Over 1980-2020, **18 years out of 41** land in the wrong decade - every year
ending in 6, 7, 8 or 9. No error, no warning, just a different answer. The
exercise counts them rather than asking you to take it on trust.

### 3. Both together

DuckDB finds a pandas DataFrame by **variable name** and reads its memory
directly:

```python
movies = pd.read_csv("data/movies.csv")

duckdb.sql("SELECT COUNT(*) FROM movies")      # `movies` is the variable
duckdb.sql("SELECT genre, COUNT(*) FROM movies GROUP BY 1").df()   # back to pandas
```

So a pipeline uses pandas for the cleaning that is awkward in SQL, then SQL
for the ranking that is awkward in pandas.

**The question:** for each decade, the 3 films that returned the most compared
to what they cost.

#### The trap: 2 171 films have no budget

```python
movies["budget"].fillna(0)                     # the tempting one-liner
movies["gross"] / movies["budget"]             # -> inf for 2 043 films
```

Dividing by a budget of zero gives `inf`, and `inf` sorts above everything.
The top of the ranking becomes pure noise. `fillna(0)` did not fill a hole,
it invented a fact: **"unknown" and "zero" are different things**.

```python
usable = movies.dropna(subset=["budget", "gross"])    # 5 436 films, 71 %
```

Drop the rows you cannot compute, and say so in the result. Then rank:

```sql
SELECT decade, name, director, ROUND(roi, 1) AS roi
FROM usable
QUALIFY ROW_NUMBER() OVER (PARTITION BY decade ORDER BY roi DESC, name) <= 3
ORDER BY decade, roi DESC
```

The answer is worth showing in a room: Paranormal Activity returned **12 890x**
its budget, The Blair Witch Project 4 144x, E.T. 75x.

The tie-break on `name` matters - without it, equal values come back in an
arbitrary order and the result is not reproducible.

#### And always ask whether dropping rows changed the conclusion

The exercise compares the average IMDb score per decade before and after the
drop. They differ: films with a known budget are the bigger productions.
**Dropping rows is never neutral.**

### Gotchas recap

| Gotcha | What to do |
| --- | --- |
| a numeric column has dtype `object` | the file contains junk - `pd.to_numeric(..., errors="coerce")` |
| `and` / `or` on a Series | use `&` `\|` `~`, parenthesise each condition |
| `fillna(0)` before a division | it invents data, and `x / 0` gives `inf` |
| `.str.contains` silently drops rows | pass `na=False` |
| `to_datetime` without `format=` | slow, and it can swap day and month |
| `WHERE COUNT(*) >= 5` | use `HAVING` - `WHERE` runs before the grouping |
| `WHERE row_number <= 3` | use `QUALIFY` - the number does not exist yet |
| `(year / 10)::INT` in SQL | `/` is float division and `::INT` rounds - use `//` |
| a top-N without a tie-break | results are not reproducible |
| dropping rows to "clean" the data | check whether it changed the answer |
