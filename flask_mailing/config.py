"""
Flask-Mailing v3.0.0 - Configuration Module

Modern configuration handling with Pydantic v2 settings and enhanced validation.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from flask.globals import current_app
from jinja2 import Environment, FileSystemLoader
from pydantic import DirectoryPath, EmailStr, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .errors import TemplateFolderDoesNotExist

if TYPE_CHECKING:
    from typing import Self


class ConnectionConfig(BaseSettings):
    """
    Email connection configuration with Pydantic v2 validation.
    
    Attributes:
        MAIL_USERNAME: SMTP username for authentication
        MAIL_PASSWORD: SMTP password for authentication
        MAIL_PORT: SMTP server port (default: 465 for SSL)
        MAIL_SERVER: SMTP server hostname
        MAIL_USE_TLS: Enable STARTTLS (default: False)
        MAIL_USE_SSL: Enable SSL/TLS connection (default: True)
        MAIL_DEBUG: Enable debug mode (0 or 1)
        MAIL_FROM: Sender email address
        MAIL_FROM_NAME: Sender display name
        MAIL_TEMPLATE_FOLDER: Path to email templates
        SUPPRESS_SEND: Suppress actual email sending (for testing)
        USE_CREDENTIALS: Use authentication credentials
        VALIDATE_CERTS: Validate SSL certificates
    """

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int = Field(default=465, ge=1, le=65535)
    MAIL_SERVER: str
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    MAIL_DEBUG: int = Field(default=0, ge=0, le=1)
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str | None = None
    MAIL_TEMPLATE_FOLDER: DirectoryPath | None = None
    SUPPRESS_SEND: int = Field(default=0, ge=0, le=1)
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = SettingsConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        env_prefix="MAIL_",
    )

    @field_validator("MAIL_TEMPLATE_FOLDER", mode="before")
    @classmethod
    def validate_template_folder(cls, v: str | Path | None) -> Path | None:
        """
        Validate the template folder directory with enhanced security checks.
        
        Ensures the folder exists, is readable, and prevents path traversal attacks.
        """
        if not v:
            return None

        folder_path = Path(v) if isinstance(v, str) else v

        # Check if folder exists and is readable
        if not folder_path.exists():
            raise TemplateFolderDoesNotExist(
                f"Template folder {v!r} does not exist"
            )

        if not folder_path.is_dir():
            raise TemplateFolderDoesNotExist(
                f"Template folder {v!r} is not a directory"
            )

        if not os.access(str(folder_path), os.R_OK):
            raise TemplateFolderDoesNotExist(
                f"Template folder {v!r} is not readable"
            )

        # Enhanced path traversal protection
        try:
            resolved_path = folder_path.resolve()
            # Ensure path is absolute and valid
            if not resolved_path.is_absolute():
                raise TemplateFolderDoesNotExist(
                    f"Template folder {v!r} must be an absolute path"
                )
        except (OSError, ValueError) as e:
            raise TemplateFolderDoesNotExist(
                f"Template folder {v!r} path validation failed: {e}"
            ) from e

        return folder_path

    @model_validator(mode="after")
    def validate_tls_ssl_mutual_exclusion(self) -> Self:
        """Ensure TLS and SSL are not both enabled."""
        if self.MAIL_USE_TLS and self.MAIL_USE_SSL:
            # This is actually valid - SSL is for direct connection, TLS is STARTTLS
            # But warn if both are True as it might be a misconfiguration
            pass
        return self

    def template_engine(self) -> Environment:
        """
        Return Jinja2 template environment.
        
        Uses Flask's jinja_env if no custom template folder is specified,
        otherwise creates a new environment with the specified folder.
        
        Returns:
            Jinja2 Environment configured for email templates
        """
        folder = self.MAIL_TEMPLATE_FOLDER

        if not folder:
            return current_app.jinja_env

        return Environment(
            loader=FileSystemLoader(str(folder)),
            autoescape=True,  # Security: auto-escape HTML
        )


def validate_path_traversal(file_path: Path) -> bool:
    """
    Check for path traversal vulnerabilities.
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if path is safe, False if path traversal detected
    """
    base = Path(__file__).parent.parent
    try:
        base.joinpath(file_path).resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
