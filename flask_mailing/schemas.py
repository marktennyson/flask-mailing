"""
Flask-Mailing v3.0.0 - Schema Module

Pydantic v2 models for email messages and validation.
"""

from __future__ import annotations

import io
import os
from enum import Enum
from mimetypes import MimeTypes
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from werkzeug.datastructures import FileStorage

from .errors import WrongFile


class MultipartSubtypeEnum(str, Enum):
    """
    MIME multipart subtypes for email messages.

    For more info about Multipart subtypes visit:
    https://en.wikipedia.org/wiki/MIME#Multipart_subtypes
    """

    mixed = "mixed"
    digest = "digest"
    alternative = "alternative"
    related = "related"
    report = "report"
    signed = "signed"
    encrypted = "encrypted"
    form_data = "form-data"
    mixed_replace = "x-mixed-replace"
    byterange = "byterange"


class Message(BaseModel):
    """
    Email message model with Pydantic v2 validation.

    Attributes:
        recipients: List of recipient email addresses
        attachments: List of file attachments (paths, FileStorage, or dicts)
        subject: Email subject line
        body: Plain text message body
        template_body: Data for Jinja2 template rendering
        template_params: Alternative way to pass template parameters
        html: HTML message body
        cc: Carbon copy recipients
        bcc: Blind carbon copy recipients
        reply_to: Reply-To addresses
        charset: Character encoding (default: utf-8)
        subtype: Content subtype (plain or html)
        multipart_subtype: MIME multipart subtype
    """

    recipients: list[EmailStr]
    attachments: list[Any] = (
        []
    )  # Processed by validator to list of (FileStorage, dict|None) tuples
    subject: str = ""
    body: str | list[Any] | None = None
    template_body: str | list[Any] | dict[str, Any] | None = None
    template_params: list[Any] | dict[str, Any] | None = None
    html: str | list[Any] | dict[str, Any] | None = None
    cc: list[EmailStr] = []
    bcc: list[EmailStr] = []
    reply_to: list[EmailStr] = []
    charset: str = "utf-8"
    subtype: str | None = None
    multipart_subtype: MultipartSubtypeEnum = MultipartSubtypeEnum.mixed

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=False,  # Allow template body assignment after render
        use_enum_values=True,
        extra="forbid",
        frozen=False,
        str_strip_whitespace=True,
    )

    @field_validator("template_params", mode="before")
    @classmethod
    def validate_template_params(
        cls, value: list[Any] | dict[str, Any] | None, info: Any
    ) -> list[Any] | dict[str, Any] | None:
        """Validate template_params field and set template_body if needed."""
        if value is not None and info.data and info.data.get("template_body") is None:
            info.data["template_body"] = value
        return value

    @field_validator("subtype", mode="before")
    @classmethod
    def validate_subtype(cls, value: str | None, info: Any) -> str | None:
        """Validate subtype field."""
        if info.data and info.data.get("template_body"):
            return "html"
        return value

    @field_validator("attachments", mode="before")
    @classmethod
    def validate_file(
        cls, v: list[FileStorage | dict[str, Any] | str]
    ) -> list[tuple[FileStorage, dict[str, Any] | None]]:
        """
        Validate and process file attachments.

        Supports:
        - File paths as strings
        - FileStorage objects
        - Dictionaries with 'file' key and optional metadata
        """
        temp: list[tuple[FileStorage, dict[str, Any] | None]] = []
        mime = MimeTypes()

        for file_entry in v:
            file_meta: dict[str, Any] | None = None

            if isinstance(file_entry, dict):
                file_meta = file_entry.copy()
                if "file" not in file_meta:
                    raise WrongFile('Missing "file" key in attachment dictionary')
                file_value = file_meta.pop("file")
            else:
                file_value = file_entry

            if isinstance(file_value, str):
                file_path = Path(file_value)
                if not _validate_attachment_path(file_path):
                    raise WrongFile(
                        f"Invalid file path for attachment: {file_value!r}. "
                        "Path may be inaccessible or contain traversal characters."
                    )

                mime_type = mime.guess_type(str(file_path))
                with file_path.open(mode="rb") as f:
                    content = f.read()

                fs = FileStorage(
                    io.BytesIO(content),
                    file_path.name,
                    content_type=mime_type[0],
                )
                temp.append((fs, file_meta))

            elif isinstance(file_value, FileStorage):
                temp.append((file_value, file_meta))
            else:
                raise WrongFile(
                    f"Invalid attachment type: {type(file_value).__name__}. "
                    "Must be a file path string or FileStorage object."
                )

        return temp

    def add_recipient(self, recipient: str) -> Literal[True]:
        """
        Add another recipient to the message.

        Args:
            recipient: Email address of recipient

        Returns:
            True on success
        """
        self.recipients.append(recipient)
        return True

    def attach(
        self,
        filename: str,
        data: bytes | str,
        content_type: str | None = None,
        disposition: str = "attachment",
        headers: dict[str, str] | None = None,
    ) -> Literal[True]:
        """
        Add an attachment to the message.

        Args:
            filename: Name for the attached file
            data: Raw file data as bytes or string
            content_type: MIME type (auto-detected if not provided)
            disposition: Content-Disposition header value
            headers: Additional headers for the attachment

        Returns:
            True on success
        """
        if content_type is None:
            mime = MimeTypes()
            content_type = mime.guess_type(filename)[0]

        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode("utf-8")

        fsob = FileStorage(
            io.BytesIO(data),
            filename,
            content_type=content_type,
        )

        # Store additional metadata for later use in message construction
        fsob.custom_disposition = disposition  # type: ignore
        if headers:
            fsob.custom_headers = headers  # type: ignore

        self.attachments.append(fsob)
        return True


def _validate_attachment_path(path: str | Path) -> bool:
    """
    Validate attachment file path for security and accessibility.

    Args:
        path: The file path to validate

    Returns:
        True if path is safe and accessible, False otherwise
    """
    try:
        path_obj = Path(path)

        # Check basic accessibility
        if not path_obj.is_file():
            return False
        if not os.access(path_obj, os.R_OK):
            return False

        # Security: Check for path traversal
        path_str = str(path_obj)
        return not (".." in path_str or "\x00" in path_str)

    except (OSError, ValueError, TypeError):
        return False
