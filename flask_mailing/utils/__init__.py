"""
Flask-Mailing v3.0.0 - Email Checking Utilities

This module provides optional email validation utilities that require
additional dependencies (redis, httpx, dnspython).

Install with: pip install flask-mailing[email-checking]
"""

from __future__ import annotations

__all__: list[str] = []

# Import email checking utilities with graceful fallback
try:
    from .email_check import DefaultChecker, WhoIsXmlApi

    __all__ = ["DefaultChecker", "WhoIsXmlApi"]
except ImportError:
    # Dependencies not installed - that's okay, these are optional
    pass
