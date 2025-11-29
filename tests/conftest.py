"""
Flask-Mailing v3.0.0 - Test Configuration

Pytest fixtures and configuration for testing.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from flask import Flask


@pytest.fixture
def default_checker() -> None:
    """Create a DefaultChecker without Redis dependency for testing."""
    pytest.skip(
        "Email checking utilities require additional dependencies. "
        "Install with: pip install flask-mailing[email-checking]"
    )


@pytest.fixture(autouse=True)
def mail_config() -> dict[str, str | int | bool | Path]:
    """Mail configuration for testing."""
    home: Path = Path(__file__).parent.parent
    html = home / "files"

    return {
        "MAIL_USERNAME": "example@test.com",
        "MAIL_PASSWORD": "strong",
        "MAIL_FROM": "example@test.com",
        "MAIL_FROM_NAME": "example",
        "MAIL_PORT": 25,
        "MAIL_SERVER": "localhost",
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": False,
        "MAIL_DEBUG": 0,
        "SUPPRESS_SEND": 1,
        "USE_CREDENTIALS": False,
        "VALIDATE_CERTS": False,
        "MAIL_TEMPLATE_FOLDER": html,
    }


@pytest.fixture(autouse=True)
def app(mail_config: dict[str, str | int | bool | Path]) -> Flask:
    """Create Flask application for testing."""
    application = Flask("test_app")
    application.secret_key = "top-secret-key"
    application.testing = True
    application.config.update(mail_config)
    return application
