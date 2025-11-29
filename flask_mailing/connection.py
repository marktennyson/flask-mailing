"""
Flask-Mailing v3.0.0 - Connection Module

Async SMTP connection handling with proper context management and error handling.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aiosmtplib
from pydantic_settings import BaseSettings

from .config import ConnectionConfig
from .errors import ConnectionErrors, PydanticClassRequired

if TYPE_CHECKING:
    from types import TracebackType


class Connection:
    """
    Manages async SMTP connections with proper resource cleanup.

    Provides an async context manager for handling SMTP connections safely.
    Supports TLS, SSL, and credential-based authentication.

    Example:
        async with Connection(config) as conn:
            await conn.session.send_message(message)
    """

    __slots__ = ("_connected", "session", "settings")

    session: aiosmtplib.SMTP
    settings: dict[str, Any]
    _connected: bool

    def __init__(self, settings: ConnectionConfig) -> None:
        """
        Initialize connection with configuration.

        Args:
            settings: ConnectionConfig instance with SMTP settings

        Raises:
            PydanticClassRequired: If settings is not a valid ConnectionConfig
        """
        if not isinstance(settings, BaseSettings):
            raise PydanticClassRequired(
                "Email configuration must be a ConnectionConfig instance. "
                "Example:\n"
                "from flask_mailing import ConnectionConfig\n"
                "conf = ConnectionConfig(\n"
                "    MAIL_USERNAME='your_username',\n"
                "    MAIL_PASSWORD='your_pass',\n"
                "    MAIL_FROM='your@email.com',\n"
                "    MAIL_PORT=587,\n"
                "    MAIL_SERVER='smtp.example.com',\n"
                "    MAIL_USE_TLS=True,\n"
                "    MAIL_USE_SSL=False\n"
                ")"
            )

        self.settings = settings.model_dump()
        self._connected = False

    async def __aenter__(self) -> Connection:
        """
        Set up an SMTP connection asynchronously.

        Returns:
            Self for use in async with statement
        """
        await self._configure_connection()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Close the SMTP connection gracefully.

        Handles cleanup even if an exception occurred during email sending.
        """
        if self._connected and not self.settings.get("SUPPRESS_SEND"):
            try:
                await self.session.quit()
            except aiosmtplib.SMTPException:
                # Connection might already be closed, ignore errors
                pass
            finally:
                self._connected = False

    async def _configure_connection(self) -> None:
        """
        Configure and establish SMTP connection.

        Raises:
            ConnectionErrors: If connection or authentication fails
        """
        try:
            self.session = aiosmtplib.SMTP(
                hostname=self.settings.get("MAIL_SERVER"),
                port=self.settings.get("MAIL_PORT"),
                use_tls=self.settings.get("MAIL_USE_SSL"),
                start_tls=self.settings.get("MAIL_USE_TLS"),
                validate_certs=self.settings.get("VALIDATE_CERTS"),
                timeout=30,  # Reasonable timeout for SMTP operations
            )

            if not self.settings.get("SUPPRESS_SEND"):
                await self.session.connect()
                self._connected = True

                if self.settings.get("USE_CREDENTIALS"):
                    username = self.settings.get("MAIL_USERNAME")
                    password = self.settings.get("MAIL_PASSWORD")

                    if not username or not password:
                        raise ConnectionErrors(
                            "MAIL_USERNAME and MAIL_PASSWORD are required "
                            "when USE_CREDENTIALS is True"
                        )

                    await self.session.login(username, password)

        except aiosmtplib.SMTPAuthenticationError as auth_error:
            raise ConnectionErrors(
                f"Authentication failed: {auth_error}. "
                "Check your username and password."
            ) from auth_error
        except aiosmtplib.SMTPConnectError as connect_error:
            raise ConnectionErrors(
                f"Could not connect to SMTP server: {connect_error}. "
                "Check your server address and port."
            ) from connect_error
        except aiosmtplib.SMTPException as smtp_error:
            raise ConnectionErrors(
                f"SMTP error: {smtp_error}. " "Check your email server configuration."
            ) from smtp_error
        except TimeoutError as timeout_error:
            raise ConnectionErrors(
                f"Connection timed out: {timeout_error}. "
                "The SMTP server may be unreachable."
            ) from timeout_error
        except Exception as error:
            raise ConnectionErrors(
                f"Unexpected connection error: {error}. "
                "Check your configuration and network."
            ) from error
