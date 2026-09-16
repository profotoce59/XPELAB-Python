"""Control flow: if, loops, match, comprehensions.

Run: python -m src.examples.control_flow
"""


def main() -> None:
    number = 7

    # Indentation defines blocks. No braces, no parentheses around the test.
    if number < 5:
        print("The number is less than 5")
    elif number == 5:
        print("The number is equal to 5")
    else:
        print("The number is greater than 5")

    # `for` always iterates over something. `range(5)` is 0, 1, 2, 3, 4.
    for i in range(5):
        print(f"For loop iteration: {i}")

    # Iterating directly over the values, not over indexes.
    for fruit in ["apple", "banana", "cherry"]:
        print(f"Fruit: {fruit}")

    # `enumerate` gives you the index along with the value.
    for index, fruit in enumerate(["apple", "banana", "cherry"]):
        print(f"{index}: {fruit}")

    # `zip` walks several collections in lockstep.
    for name, role in zip(["Keanu", "Laurence"], ["Neo", "Morpheus"]):
        print(f"{name} plays {role}")

    count = 0
    while count < 5:
        print(f"While loop count: {count}")
        count += 1

    # `break` and `continue` work as expected. Python also has a rarely used
    # `else` on loops: it runs only if the loop ended WITHOUT a break.
    for i in range(10):
        if i == 3:
            break
    else:
        print("this is not printed, the loop was broken")

    # `match` (Python 3.10+) is the equivalent of Rust's `match`.
    # It is NOT exhaustive: forgetting a case is not a compile error,
    # so a `case _` fallback is on you.
    match number:
        case 1:
            result = "One"
        case 2:
            result = "Two"
        case 3 | 4 | 5:
            result = "Three, Four, or Five"
        case _:
            result = "Something else"
    print(f"Match result: {result}")

    # match can destructure, which is where it beats a chain of if/elif.
    point = (0, 5)
    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"On the Y axis at {y}")
        case (x, 0):
            print(f"On the X axis at {x}")
        case (x, y):
            print(f"At ({x}, {y})")

    day = 3
    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
            5: "Friday", 6: "Saturday", 7: "Sunday"}
    # A dict with a default is often cleaner than a big match.
    print(f"Day {day} is {days.get(day, 'Invalid day')}")

    # Comprehensions: the idiomatic way to build a collection from another.
    # Rust: (1..=5).map(|x| x * x).collect::<Vec<_>>()
    squares = [x * x for x in range(1, 6)]
    print(f"Squares: {squares}")

    even_squares = [x * x for x in range(1, 11) if x % 2 == 0]
    print(f"Even squares: {even_squares}")

    by_length = {word: len(word) for word in ["Neo", "Morpheus", "Trinity"]}
    print(f"Dict comprehension: {by_length}")

    # Ternary expression: `value_if_true if condition else value_if_false`
    label = "even" if number % 2 == 0 else "odd"
    print(f"{number} is {label}")


if __name__ == "__main__":
    main()
