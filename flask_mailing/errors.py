"""
Flask-Mailing v3.0.0 - Exception Classes

Modern exception hierarchy for Flask-Mailing with proper
exception chaining and detailed error messages.
"""

from __future__ import annotations


class FlaskMailingError(Exception):
    """Base exception for all Flask-Mailing errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r})"


class ConnectionErrors(FlaskMailingError):
    """Raised when SMTP connection fails."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Connection error: {message}")


class WrongFile(FlaskMailingError):
    """Raised when file attachment is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid file: {message}")


class PydanticClassRequired(FlaskMailingError):
    """Raised when a Pydantic model is required but not provided."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TemplateFolderDoesNotExist(FlaskMailingError):
    """Raised when template folder path is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Template folder error: {message}")


class ConfigurationError(FlaskMailingError):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Configuration error: {message}")


class SecurityError(FlaskMailingError):
    """Raised when a security check fails."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Security error: {message}")
