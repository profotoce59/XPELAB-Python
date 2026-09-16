"""Custom errors.

Rust defines a `struct XpelabError` and implements `Display` on it.
Python has an exception hierarchy: every error inherits from `Exception`,
and `__str__` plays the role of `Display`.
"""


class XpelabError(Exception):
    """Base error for the application."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
