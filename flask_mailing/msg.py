"""
Flask-Mailing v3.0.0 - Message Construction Module

MIME message construction with support for HTML, attachments, and templates.
"""

from __future__ import annotations

import time
import warnings
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


class MailMsg:
    """
    MIME message builder for email construction.

    Constructs properly formatted email messages with support for:
    - Plain text and HTML content
    - Multiple recipients (To, CC, BCC)
    - File attachments with custom MIME types
    - Template-rendered content
    - Custom headers and charset

    Attributes:
        subject: Email subject header
        recipients: List of primary recipient email addresses
        body: Plain text message body
        template_body: Rendered template content
        html: HTML message body
        cc: Carbon copy recipients
        bcc: Blind carbon copy recipients
        reply_to: Reply-To addresses
        attachments: List of file attachments
        charset: Character encoding (default: utf-8)
        subtype: Content subtype (plain or html)
        multipart_subtype: MIME multipart subtype
    """

    __slots__ = (
        "attachments",
        "bcc",
        "body",
        "cc",
        "charset",
        "html",
        "message",
        "msgId",
        "multipart_subtype",
        "recipients",
        "reply_to",
        "subject",
        "subtype",
        "template_body",
    )

    def __init__(self, **entries: Any) -> None:
        """
        Initialize message with provided values.

        Args:
            **entries: Message attributes as keyword arguments
        """
        # Set default values
        self.subject: str = ""
        self.recipients: list[str] = []
        self.body: str | None = None
        self.template_body: str | None = None
        self.html: str | None = None
        self.cc: list[str] = []
        self.bcc: list[str] = []
        self.reply_to: list[str] = []
        self.attachments: list[tuple[FileStorage, dict[str, Any] | None]] = []
        self.charset: str = "utf-8"
        self.subtype: str | None = None
        self.multipart_subtype: str = "mixed"  # Default MIME multipart subtype
        self.message: MIMEMultipart

        # Update with provided values
        for key, value in entries.items():
            if hasattr(self, key):
                # Handle enum values - extract string value
                if key == "multipart_subtype" and hasattr(value, "value"):
                    setattr(self, key, value.value)
                else:
                    setattr(self, key, value)

        self.msgId = make_msgid()

    def _mimetext(self, text: str, subtype: str = "plain") -> MIMEText:
        """
        Create a MIMEText object.

        Args:
            text: Text content
            subtype: MIME subtype (plain or html)

        Returns:
            MIMEText object with specified content and subtype
        """
        return MIMEText(text, _subtype=subtype, _charset=self.charset)

    async def attach_file(
        self,
        attachment: list[tuple[FileStorage, dict[str, Any] | None]],
    ) -> None:
        """
        Attach files to the message.

        Args:
            attachment: List of (FileStorage, metadata) tuples
        """
        for file, file_meta in attachment:
            # Determine MIME type
            if (
                file_meta
                and isinstance(file_meta, dict)
                and "mime_type" in file_meta
                and "mime_subtype" in file_meta
            ):
                part = MIMEBase(
                    _maintype=file_meta["mime_type"],
                    _subtype=file_meta["mime_subtype"],
                )
            else:
                part = MIMEBase(_maintype="application", _subtype="octet-stream")

            part.set_payload(file.read())
            encode_base64(part)

            filename = file.filename

            # Handle Unicode filenames
            try:
                if filename:
                    filename.encode("ascii")
            except UnicodeEncodeError:
                if filename:
                    filename = filename.encode("utf8").decode("utf8")

            filename_header = ("UTF8", "", filename or "attachment")
            part.add_header(
                "Content-Disposition", "attachment", filename=filename_header
            )

            # Add custom headers if provided
            if file_meta and isinstance(file_meta, dict) and "headers" in file_meta:
                headers = file_meta["headers"]
                if isinstance(headers, dict):
                    for header, value in headers.items():
                        part.add_header(header, value)

            self.message.attach(part)

    async def _message(self, sender: str) -> MIMEMultipart:
        """
        Build the complete email message.

        Args:
            sender: Sender email address (with optional display name)

        Returns:
            Complete MIMEMultipart message ready for sending

        Raises:
            ValueError: If both template_body and html are set
        """
        self.message = MIMEMultipart(self.multipart_subtype)
        self.message.set_charset(self.charset)

        # Set standard headers
        self.message["Date"] = formatdate(time.time(), localtime=True)
        self.message["Message-ID"] = self.msgId
        self.message["To"] = ", ".join(self.recipients)
        self.message["From"] = sender

        if self.subject:
            self.message["Subject"] = self.subject

        if self.cc:
            self.message["Cc"] = ", ".join(self.cc)

        if self.bcc:
            self.message["Bcc"] = ", ".join(self.bcc)

        if self.reply_to:
            self.message["Reply-To"] = ", ".join(self.reply_to)

        # Attach body content
        if self.body:
            self.message.attach(self._mimetext(self.body))

        # Handle template body or HTML content
        if self.template_body or self.body:
            if not self.html and self.subtype == "html":
                if self.body:
                    warnings.warn(
                        "Use 'template_body' instead of 'body' to pass data "
                        "into Jinja2 templates",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                content = (self.template_body or self.body) or ""
                subtype = self.subtype or "html"
                self.message.attach(self._mimetext(str(content), subtype))
            elif self.template_body:
                raise ValueError(
                    "Cannot send both Jinja2 template content and HTML content. "
                    "Use either 'template_body' with a template or 'html' for raw HTML."
                )
        elif self.html:
            self.message.attach(self._mimetext(self.html, "html"))

        # Attach files
        if self.attachments:
            await self.attach_file(self.attachments)

        return self.message

    async def as_string(self, sender: str = "") -> str:
        """
        Get message as string.

        Args:
            sender: Sender email address

        Returns:
            Message as formatted string
        """
        msg = await self._message(sender)
        return msg.as_string()

    async def as_bytes(self, sender: str = "") -> bytes:
        """
        Get message as bytes.

        Args:
            sender: Sender email address

        Returns:
            Message as bytes
        """
        msg = await self._message(sender)
        return msg.as_bytes()

    def __str__(self) -> str:
        """String representation of the message."""
        return f"<MailMsg: {self.subject}>"

    def __repr__(self) -> str:
        """Detailed representation of the message."""
        return (
            f"MailMsg(subject={self.subject!r}, "
            f"recipients={self.recipients!r}, "
            f"msgId={self.msgId!r})"
        )
