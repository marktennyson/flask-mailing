"""
Flask-Mailing v3.0.0 - Configuration Tests
"""

from __future__ import annotations

from flask_mailing.config import ConnectionConfig


def test_configuration(mail_config: dict) -> None:
    """Test ConnectionConfig validation."""
    conf = ConnectionConfig.model_validate(mail_config)
    assert conf.MAIL_USERNAME == "example@test.com"
    assert conf.MAIL_PORT == 25


def test_configuration_defaults(mail_config: dict) -> None:
    """Test ConnectionConfig default values."""
    conf = ConnectionConfig.model_validate(mail_config)
    assert conf.USE_CREDENTIALS is False
    assert conf.VALIDATE_CERTS is False
    assert conf.MAIL_USE_TLS is False
    assert conf.MAIL_USE_SSL is False
