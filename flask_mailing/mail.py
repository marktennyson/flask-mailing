"""
Flask-Mailing v3.0.0 - Mail Module

Core mail sending functionality with async support and Flask integration.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import blinker
from pydantic import BaseModel, EmailStr

from .config import ConnectionConfig
from .connection import Connection
from .errors import PydanticClassRequired
from .msg import MailMsg
from .schemas import Message

if TYPE_CHECKING:
    from email.mime.multipart import MIMEMultipart

    from flask import Flask
    from jinja2 import Template

__version_info__ = (3, 0, 0)
__version__ = ".".join(str(v) for v in __version_info__)


# Signal for email dispatch events
signals = blinker.Namespace()
email_dispatched = signals.signal(
    "email-dispatched",
    doc="""
    Signal sent when an email is dispatched. This signal will also be sent
    in testing mode, even though the email will not actually be sent.
    
    Example:
        @email_dispatched.connect
        def log_email(message):
            print(f"Email sent: {message['Subject']}")
    """,
)


class _MailMixin:
    """Mixin providing common mail functionality."""

    name: str = "Flask Mailing"
    version: str = __version__

    @contextmanager
    def record_messages(self) -> Generator[list[MIMEMultipart], None, None]:
        """
        Context manager to record all messages sent.
        
        Use in unit tests to capture sent emails without actually sending them.
        
        Example:
            with mail.record_messages() as outbox:
                response = app.test_client.get("/email-sending-view/")
                assert len(outbox) == 1
                assert outbox[0]["Subject"] == "testing"
        
        Yields:
            List that will be populated with sent message objects
            
        Raises:
            RuntimeError: If blinker is not installed
        """
        if not email_dispatched:
            raise RuntimeError("blinker must be installed for message recording")

        outbox: list[MIMEMultipart] = []

        def _record(message: MIMEMultipart) -> None:
            outbox.append(message)

        email_dispatched.connect(_record)

        try:
            yield outbox
        finally:
            email_dispatched.disconnect(_record)


class Mail(_MailMixin):
    """
    Flask mail system for sending individual and bulk emails with attachments.
    
    Provides async email sending with full Flask integration, template support,
    and comprehensive error handling.
    
    Attributes:
        config: ConnectionConfig instance with SMTP settings
        
    Example:
        app = Flask(__name__)
        app.config.update(
            MAIL_USERNAME="user@example.com",
            MAIL_PASSWORD="password",
            MAIL_SERVER="smtp.example.com",
            MAIL_PORT=587,
            MAIL_USE_TLS=True,
        )
        mail = Mail(app)
        
        @app.post("/send")
        async def send():
            message = Message(
                subject="Hello",
                recipients=["recipient@example.com"],
                body="Hello World!"
            )
            await mail.send_message(message)
    """

    config: ConnectionConfig

    def __init__(self, app: Flask | None = None) -> None:
        """
        Initialize Mail extension.
        
        Args:
            app: Optional Flask application. If provided, init_app is called.
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize the Mail extension with a Flask application.
        
        Reads configuration from Flask app.config and sets up the mail system.
        
        Args:
            app: Flask application instance
            
        Raises:
            ValueError: If required configuration is missing
        """
        # Validate required config values
        required_configs = ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_SERVER"]
        missing = [key for key in required_configs if not app.config.get(key)]
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}"
            )

        # Determine sender email
        mail_from = app.config.get(
            "MAIL_FROM",
            app.config.get("MAIL_DEFAULT_SENDER", app.config.get("MAIL_USERNAME")),
        )
        if not mail_from:
            raise ValueError(
                "MAIL_FROM, MAIL_DEFAULT_SENDER, or MAIL_USERNAME must be configured"
            )

        self.config = ConnectionConfig(
            MAIL_USERNAME=app.config["MAIL_USERNAME"],
            MAIL_PASSWORD=app.config["MAIL_PASSWORD"],
            MAIL_PORT=app.config.get("MAIL_PORT", 465),
            MAIL_SERVER=app.config["MAIL_SERVER"],
            MAIL_USE_TLS=app.config.get("MAIL_USE_TLS", False),
            MAIL_USE_SSL=app.config.get("MAIL_USE_SSL", True),
            MAIL_DEBUG=app.config.get("MAIL_DEBUG", 0),
            MAIL_FROM_NAME=app.config.get("MAIL_FROM_NAME"),
            MAIL_TEMPLATE_FOLDER=app.config.get("MAIL_TEMPLATE_FOLDER"),
            SUPPRESS_SEND=app.config.get("SUPPRESS_SEND", 0),
            USE_CREDENTIALS=app.config.get("USE_CREDENTIALS", True),
            VALIDATE_CERTS=app.config.get("VALIDATE_CERTS", True),
            MAIL_FROM=mail_from,
        )

        # Register extension with Flask
        app.extensions["mailing"] = self

    async def get_mail_template(
        self,
        env_path: Any,
        template_name: str,
    ) -> Template:
        """
        Load a mail template from the configured template folder.
        
        Args:
            env_path: Jinja2 Environment instance
            template_name: Name of the template file
            
        Returns:
            Loaded Jinja2 Template
        """
        return env_path.get_template(template_name)

    @staticmethod
    def make_dict(data: Any) -> dict[str, Any]:
        """
        Convert data to dictionary for template rendering.
        
        Args:
            data: Data to convert (dict, BaseModel, or dict-like object)
            
        Returns:
            Dictionary representation of data
            
        Raises:
            ValueError: If data cannot be converted to dict
        """
        if isinstance(data, dict):
            return data
        try:
            return dict(data)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Unable to build template data dictionary - "
                f"{type(data).__name__} is an invalid source data type"
            ) from e

    async def __prepare_message(
        self,
        message: Message,
        template: Template | None = None,
    ) -> MIMEMultipart:
        """
        Prepare email message for sending.
        
        Args:
            message: Message instance with email content
            template: Optional Jinja2 template for HTML rendering
            
        Returns:
            Prepared MIMEMultipart message ready for sending
        """
        if template is not None:
            template_body = message.template_body
            if template_body and not message.html:
                if isinstance(template_body, list):
                    message.template_body = template.render({"body": template_body})
                else:
                    template_data = self.make_dict(template_body)
                    message.template_body = template.render(**template_data)

                message.subtype = "html"
            elif message.html:
                if isinstance(template_body, list):
                    message.template_body = template.render({"body": template_body})
                elif template_body:
                    template_data = self.make_dict(template_body)
                    message.template_body = template.render(**template_data)

        msg = MailMsg(**message.model_dump())

        # Build sender string
        if self.config.MAIL_FROM_NAME:
            sender = f"{self.config.MAIL_FROM_NAME} <{self.config.MAIL_FROM}>"
        else:
            sender = str(self.config.MAIL_FROM)

        return await msg._message(sender)

    async def send_message(
        self,
        message: Message,
        template_name: str | None = None,
    ) -> None:
        """
        Send an email message.
        
        Args:
            message: Message instance with email content
            template_name: Optional template file name for HTML rendering
            
        Raises:
            PydanticClassRequired: If message is not a Message instance
            
        Example:
            message = Message(
                subject="Flask-Mailing module",
                recipients=["user@example.com"],
                body="This is the basic email body",
            )
            await mail.send_message(message)
        """
        if not isinstance(message, BaseModel):
            raise PydanticClassRequired(
                "Message must be a Message class instance. Example:\n"
                "from flask_mailing import Message\n"
                "message = Message(\n"
                "    subject='Subject',\n"
                "    recipients=['recipient@example.com'],\n"
                "    body='Hello World',\n"
                ")"
            )

        if template_name:
            template = await self.get_mail_template(
                self.config.template_engine(), template_name
            )
            msg = await self.__prepare_message(message, template)
        else:
            msg = await self.__prepare_message(message)

        async with Connection(self.config) as session:
            if not self.config.SUPPRESS_SEND:
                await session.session.send_message(msg)

            email_dispatched.send(msg)

    async def send_mail(
        self,
        subject: str,
        message: str,
        recipients: list[EmailStr],
        html_message: str | None = None,
        **msgkwargs: Any,
    ) -> None:
        """
        Send a simple email using keyword arguments.
        
        This is a convenience method for quick email sending without
        creating a Message object manually.
        
        Args:
            subject: Email subject line
            message: Plain text email body
            recipients: List of recipient email addresses
            html_message: Optional HTML email body
            **msgkwargs: Additional Message parameters
            
        Example:
            await mail.send_mail(
                subject="Hello",
                message="Plain text body",
                recipients=["user@example.com"],
                html_message="<h1>HTML body</h1>"
            )
        """
        msg_obj = Message(
            subject=subject,
            recipients=recipients,
            body=message,
            html=html_message,
            **msgkwargs,
        )
        await self.send_message(msg_obj)

    async def send_mass_mail(
        self,
        datatuple: tuple[tuple[str, str, list[EmailStr]], ...],
    ) -> None:
        """
        Send multiple emails efficiently.
        
        Args:
            datatuple: Tuple of (subject, message, recipients) tuples
            
        Example:
            emails = (
                ("Subject 1", "Message 1", ["user1@example.com"]),
                ("Subject 2", "Message 2", ["user2@example.com"]),
            )
            await mail.send_mass_mail(emails)
        """
        for subject, message, recipients in datatuple:
            await self.send_mail(subject, message, recipients)
