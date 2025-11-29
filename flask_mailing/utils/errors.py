"""
Flask-Mailing v3.0.0 - Utility Exceptions

Exception classes for email checking utilities.
"""

from __future__ import annotations


class InvalidEmail(Exception):
    """Raised when an email address is invalid."""

    def __init__(self, message: str = "Invalid email address") -> None:
        self.message = message
        super().__init__(self.message)


class ApiError(Exception):
    """Raised when an external API call fails."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DBProvaiderError(Exception):
    """Raised when database provider operations fail."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
