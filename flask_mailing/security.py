"""
Flask-Mailing v3.0.0 - Security Module

Security enhancements including rate limiting, email validation,
and protection against common attacks.
"""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from typing import Any, ClassVar

from pydantic import BaseModel, EmailStr, Field


class RateLimiter:
    """
    Async-safe in-memory rate limiter for email sending.

    Implements a sliding window rate limiting algorithm to prevent
    email sending abuse. For production use with multiple workers,
    consider using Redis-based rate limiting.

    Attributes:
        max_emails: Maximum emails allowed per time window
        window_seconds: Time window duration in seconds

    Example:
        rate_limiter = RateLimiter(max_emails=100, window_seconds=3600)

        if await rate_limiter.is_allowed(client_ip):
            await mail.send_message(message)
        else:
            raise RateLimitExceeded("Too many emails sent")
    """

    __slots__ = ("_buckets", "_lock", "max_emails", "window_seconds")

    def __init__(
        self,
        max_emails: int = 100,
        window_seconds: int = 3600,
    ) -> None:
        """
        Initialize rate limiter.

        Args:
            max_emails: Maximum emails allowed per window (default: 100)
            window_seconds: Time window in seconds (default: 3600 = 1 hour)
        """
        self.max_emails = max_emails
        self.window_seconds = window_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, identifier: str) -> bool:
        """
        Check if the identifier is allowed to send an email.

        Args:
            identifier: Unique identifier (e.g., IP address, user ID)

        Returns:
            True if allowed, False if rate limited
        """
        async with self._lock:
            current_time = time.time()

            # Clean expired entries
            self._buckets[identifier] = [
                timestamp
                for timestamp in self._buckets[identifier]
                if current_time - timestamp < self.window_seconds
            ]

            # Check if under limit
            if len(self._buckets[identifier]) >= self.max_emails:
                return False

            # Add current request
            self._buckets[identifier].append(current_time)
            return True

    async def get_remaining(self, identifier: str) -> int:
        """
        Get remaining emails allowed for identifier.

        Args:
            identifier: Unique identifier

        Returns:
            Number of remaining emails allowed in current window
        """
        async with self._lock:
            current_time = time.time()

            # Clean expired entries
            self._buckets[identifier] = [
                timestamp
                for timestamp in self._buckets[identifier]
                if current_time - timestamp < self.window_seconds
            ]

            return max(0, self.max_emails - len(self._buckets[identifier]))

    async def reset(self, identifier: str) -> None:
        """
        Reset rate limit for an identifier.

        Args:
            identifier: Unique identifier to reset
        """
        async with self._lock:
            self._buckets[identifier] = []

    async def get_reset_time(self, identifier: str) -> float | None:
        """
        Get time until rate limit resets for identifier.

        Args:
            identifier: Unique identifier

        Returns:
            Seconds until reset, or None if not rate limited
        """
        async with self._lock:
            if not self._buckets[identifier]:
                return None

            oldest = min(self._buckets[identifier])
            reset_time = oldest + self.window_seconds - time.time()
            return max(0, reset_time)


class EmailSecurityValidator(BaseModel):
    """
    Enhanced email validation with security checks.

    Validates email addresses against common security concerns including
    disposable email providers and role-based addresses.

    Attributes:
        email: Email address to validate
        allow_disposable: Whether to allow disposable email addresses
        allow_role_based: Whether to allow role-based emails (admin@, etc.)

    Example:
        validator = EmailSecurityValidator(
            email="user@example.com",
            allow_disposable=False,
            allow_role_based=True
        )

        result = validator.validate_security()
        if not result["is_valid"]:
            print(f"Validation failed: {result['warnings']}")
    """

    email: EmailStr
    allow_disposable: bool = Field(
        default=False,
        description="Allow disposable email addresses",
    )
    allow_role_based: bool = Field(
        default=True,
        description="Allow role-based emails (admin@, support@, etc.)",
    )

    # Common disposable email domains
    DISPOSABLE_DOMAINS: ClassVar[frozenset[str]] = frozenset(
        {
            "10minutemail.com",
            "guerrillamail.com",
            "mailinator.com",
            "tempmail.org",
            "yopmail.com",
            "sharklasers.com",
            "throwaway.email",
            "temp-mail.org",
            "fakeinbox.com",
            "trashmail.com",
            "dispostable.com",
            "mailnesia.com",
            "tempail.com",
            "getnada.com",
        }
    )

    # Common role-based email prefixes
    ROLE_BASED_PREFIXES: ClassVar[frozenset[str]] = frozenset(
        {
            "admin",
            "administrator",
            "support",
            "help",
            "info",
            "contact",
            "sales",
            "marketing",
            "noreply",
            "no-reply",
            "webmaster",
            "postmaster",
            "hostmaster",
            "abuse",
            "security",
            "billing",
            "jobs",
            "careers",
            "hr",
            "legal",
            "privacy",
        }
    )

    def validate_security(self) -> dict[str, Any]:
        """
        Perform security validation on the email address.

        Returns:
            Dictionary containing validation results:
            - email: The validated email
            - is_valid: Whether the email passes all checks
            - is_disposable: Whether the domain is a known disposable provider
            - is_role_based: Whether the local part is a role-based prefix
            - domain: The email domain
            - local_part: The local part of the email
            - warnings: List of warning messages
        """
        email_str = str(self.email)
        parts = email_str.split("@")
        domain = parts[1].lower() if len(parts) > 1 else ""
        local_part = parts[0].lower() if parts else ""

        results: dict[str, Any] = {
            "email": email_str,
            "is_valid": True,
            "is_disposable": domain in self.DISPOSABLE_DOMAINS,
            "is_role_based": local_part in self.ROLE_BASED_PREFIXES,
            "domain": domain,
            "local_part": local_part,
            "warnings": [],
        }

        # Check disposable email policy
        if results["is_disposable"] and not self.allow_disposable:
            results["is_valid"] = False
            results["warnings"].append("Disposable email addresses are not allowed")

        # Check role-based email policy
        if results["is_role_based"] and not self.allow_role_based:
            results["is_valid"] = False
            results["warnings"].append("Role-based email addresses are not allowed")

        # Check for suspicious patterns
        if "+test" in local_part or "+spam" in local_part:
            results["warnings"].append("Potentially test or spam email address")

        # Check domain length
        if len(domain) > 50:
            results["warnings"].append("Unusually long domain name")

        # Check for numeric-only local parts (often spam)
        if local_part.isdigit():
            results["warnings"].append("Numeric-only email addresses are suspicious")

        return results


def sanitize_email_content(content: str, max_length: int = 1_000_000) -> str:
    """
    Sanitize email content to prevent injection attacks.

    Removes or escapes potentially dangerous patterns that could be
    used for SMTP injection or header manipulation.

    Args:
        content: Raw email content
        max_length: Maximum content length (default: 1MB)

    Returns:
        Sanitized content string
    """
    if not isinstance(content, str):
        content = str(content)

    # Remove potential SMTP injection patterns
    # These patterns could be used to inject additional headers
    dangerous_patterns = [
        ("\r\n", " "),
        ("\r", " "),
        ("\n", " "),
    ]

    sanitized = content
    for pattern, replacement in dangerous_patterns:
        sanitized = sanitized.replace(pattern, replacement)

    # Limit content length to prevent DoS
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "... [content truncated for security]"

    return sanitized.strip()


def validate_attachment_security(
    filename: str,
    content_type: str | None = None,
) -> dict[str, Any]:
    """
    Validate attachment security.

    Checks attachments for potentially dangerous file types and patterns.

    Args:
        filename: Name of the attachment file
        content_type: MIME type of the attachment (optional)

    Returns:
        Dictionary containing:
        - filename: The validated filename
        - is_safe: Whether the attachment is considered safe
        - warnings: List of warning messages
    """
    results: dict[str, Any] = {
        "filename": filename,
        "is_safe": True,
        "warnings": [],
    }

    # Dangerous file extensions
    dangerous_extensions = frozenset(
        {
            ".exe",
            ".bat",
            ".cmd",
            ".com",
            ".pif",
            ".scr",
            ".vbs",
            ".js",
            ".jar",
            ".sh",
            ".ps1",
            ".msi",
            ".dll",
            ".sys",
            ".reg",
            ".hta",
            ".cpl",
            ".msc",
            ".inf",
            ".scf",
            ".lnk",
            ".ws",
            ".wsf",
            ".wsh",
        }
    )

    # Extract extension
    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension in dangerous_extensions:
        results["is_safe"] = False
        results["warnings"].append(f"Potentially dangerous file extension: {extension}")

    # Check filename length
    if len(filename) > 255:
        results["is_safe"] = False
        results["warnings"].append("Filename too long")

    # Check for path traversal in filename
    if ".." in filename or "/" in filename or "\\" in filename:
        results["is_safe"] = False
        results["warnings"].append("Filename contains path traversal characters")

    # Check for null bytes
    if "\x00" in filename:
        results["is_safe"] = False
        results["warnings"].append("Filename contains null bytes")

    # Validate content type if provided
    if content_type:
        suspicious_types = frozenset(
            {
                "application/x-executable",
                "application/x-msdownload",
                "application/x-msdos-program",
                "application/x-sh",
                "application/x-shellscript",
            }
        )

        if content_type in suspicious_types:
            results["warnings"].append(f"Suspicious content type: {content_type}")

    return results


def is_valid_email_header(header_value: str) -> bool:
    """
    Validate email header value for injection attacks.

    Args:
        header_value: The header value to validate

    Returns:
        True if the header value is safe, False otherwise
    """
    # Check for newline characters that could inject headers
    if "\r" in header_value or "\n" in header_value:
        return False

    # Check for null bytes
    return "\x00" not in header_value
