"""
# ✉️ Flask-Mailing v3.0.0 - 2026 Production Ready!

Modern, secure, and high-performance SMTP mail sending for Flask applications.

## 🚀 2026-Ready Features

Flask-Mailing v3.0.0 is built for the future with:

### 🔧 Modern Python Support
- **Python 3.10+** required (3.14 ready!)
- **Modern type hints** with union operators (|) and built-in generics
- **Full async/await** support with proper context managers
- **Enhanced error handling** with exception chaining

### 🛡️ Advanced Security
- **Rate limiting** to prevent abuse
- **Enhanced email validation** with disposable email detection
- **Path traversal protection** for attachments
- **Content sanitization** to prevent injection attacks
- **Attachment security validation**

### ⚡ Performance & Reliability
- **Flask 3.1+** compatibility
- **Pydantic v2.11+** with modern validators
- **Connection pooling** and timeout handling
- **Improved async patterns**
- **Better error reporting**

### 🔗 Important Links

#### ❤️ [Github](https://github.com/marktennyson/flask-mailing)
#### 📄 [Documentation](https://marktennyson.github.io/flask-mailing)
#### 🐍 [PYPI](https://pypi.org/project/flask-mailing)

## 🔨 Installation

```bash
# Python 3.10+ required
pip install flask-mailing>=3.0.0
```

## 🦮 Quick Start (2026 Style)

```python
from __future__ import annotations

from flask import Flask, jsonify
from flask_mailing import Mail, Message, RateLimiter


app = Flask(__name__)

# Modern configuration
app.config.update(
    MAIL_USERNAME="your.email@example.com",
    MAIL_PASSWORD="your_secure_app_password",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_FROM="your.email@example.com",
    MAIL_FROM_NAME="Flask-Mailing v3.0.0"
)

# Initialize with modern patterns
mail = Mail(app)
rate_limiter = RateLimiter(max_emails=100, window_seconds=3600)


@app.post("/send-email")
async def modern_send() -> dict[str, str]:
    # Rate limiting check
    client_ip = request.remote_addr
    if not await rate_limiter.is_allowed(client_ip):
        return jsonify({"error": "Rate limit exceeded"}), 429

    # Modern message creation with type safety
    message = Message(
        subject="Flask-Mailing v3.0.0 - 2026 Ready!",
        recipients=["recipient@example.com"],
        body="<h1>Welcome to the future of Flask email!</h1>",
        subtype="html"
    )

    await mail.send_message(message)
    return {"message": "Email sent successfully!", "version": "3.0.0"}
```

## 🛡️ Security Features

```python
from flask_mailing import EmailSecurityValidator

# Validate email security
validator = EmailSecurityValidator(
    email="user@example.com",
    allow_disposable=False,
    allow_role_based=True
)

security_check = validator.validate_security()
if not security_check["is_valid"]:
    print(f"Email validation failed: {security_check['warnings']}")
```

## 🪜 Advanced Examples

Check out the [examples directory](https://github.com/marktennyson/flask-mailing/tree/main/examples) for:
- **Modern Flask 3.1+ patterns**
- **Async context managers**
- **Rate limiting integration**
- **Security best practices**
- **Performance optimization**

## 📝 LICENSE

[MIT](LICENSE)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .config import ConnectionConfig
from .mail import Mail
from .schemas import Message, MultipartSubtypeEnum
from .security import EmailSecurityValidator, RateLimiter

# Import utils for type checking only
if TYPE_CHECKING:
    from . import utils as utils  # noqa: F401

__author__ = "Aniket Sarkar"
__email__ = "aniketsarkar@yahoo.com"
__version__ = "3.0.0"
__version_info__ = (3, 0, 0)
__license__ = "MIT"

__all__ = [
    # Core classes
    "Mail",
    "Message",
    "ConnectionConfig",
    # Enums
    "MultipartSubtypeEnum",
    # Security
    "RateLimiter",
    "EmailSecurityValidator",
    # Metadata
    "__version__",
    "__version_info__",
    "__author__",
]
