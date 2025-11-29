# ✉️ Flask-Mailing v3.0.0 🚀
![Flask mail logo](https://github.com/marktennyson/flask-mailing/blob/main/logo/flask-mailing-logo-cropped.png?raw=true)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.1+](https://img.shields.io/badge/flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![Pydantic v2.11+](https://img.shields.io/badge/pydantic-2.11+-red.svg)](https://pydantic.dev/)
[![Async Ready](https://img.shields.io/badge/async-ready-orange.svg)](https://docs.python.org/3/library/asyncio.html)
[![Security Enhanced](https://img.shields.io/badge/security-enhanced-purple.svg)](#-security-features)

## 🌟 The Future of Flask Email - Available Today!

**Flask-Mailing v3.0.0** represents the pinnacle of modern Python email handling. Built for **2026 and beyond**, it combines cutting-edge Python 3.10+ features, Flask 3.1+ compatibility, and enterprise-grade security into one powerful package.

## ✨ What's Revolutionary in v3.0.0

### 🎯 Modern Python Excellence
- **✅ Python 3.10+ Required** - Modern union syntax (`str | None`) and built-in generics
- **✅ Python 3.14 Ready** - Future-proof architecture
- **✅ Type Safety First** - Full type hints with mypy validation
- **✅ Performance Optimized** - Built for modern Python performance gains

### 🛡️ Enterprise Security
- **🔒 Rate Limiting** - Prevent abuse with built-in rate limiting
- **🛡️ Email Security Validation** - Detect and block disposable/malicious emails  
- **🔐 Path Traversal Protection** - Enhanced file attachment security
- **🚨 Content Sanitization** - Prevent injection attacks
- **🔍 Security Scanning** - Automated vulnerability detection

### ⚡ Next-Gen Architecture
- **🔄 Modern Async Patterns** - Proper context managers and error handling
- **📦 Pydantic v2.11+** - Latest validation with enhanced performance
- **🏗️ Modern Build System** - Ruff, Black, isort, mypy integration
- **🐳 Container Ready** - Docker support with security best practices

## 📋 Requirements

- **Python 3.10+** (3.14 compatible!)
- **Flask 3.1+** with async support
- **Modern development environment**

## 🔧 Installation

```bash
# 2026-Ready Installation (Python 3.10+ required)
pip install flask-mailing>=3.0.0

# With enhanced security features
pip install flask-mailing[email-checking]

# Full development setup
pip install flask-mailing[dev,email-checking]
```

### 📦 Development Installation
```bash
git clone https://github.com/marktennyson/flask-mailing.git
cd flask-mailing
pip install -e ".[dev,email-checking]"
```

## 🚀 Modern Quick Start

### Flask 3.1+ with Modern Python Features

```python
from flask import Flask, jsonify
from flask_mailing import Mail, Message

app = Flask(__name__)

# Configuration for Flask 3.x
app.config.update(
    MAIL_USERNAME="your.email@gmail.com",
    MAIL_PASSWORD="your_app_password", 
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_DEFAULT_SENDER="your.email@gmail.com",
    MAIL_FROM_NAME="Your App Name"
)

mail = Mail(app)

@app.post("/send-email")
async def send_email():
    message = Message(
        subject="Flask-Mailing v3.0.0 Test",
        recipients=["recipient@example.com"],
        body="Hello from Flask-Mailing v3.0.0! 🚀\n\nNow with Python 3.10-3.14 and Flask 3.x support!",
        subtype="plain"
    )
    
    await mail.send_message(message)
    return jsonify({"status": "Email sent successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
```

### HTML Email with Modern Syntax

```python
@app.post("/send-html")
async def send_html():
    html_content = """
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h1 style="color: #2c3e50;">Welcome to Flask-Mailing v3.0.0!</h1>
            <p>This email was sent using the modernized Flask-Mailing library.</p>
            <ul>
                <li>✅ Python 3.10-3.14 compatible</li>
                <li>✅ Flask 3.1+ ready</li>
                <li>✅ Enhanced performance</li>
            </ul>
        </body>
    </html>
    """
    
    message = Message(
        subject="🚀 Flask-Mailing v3.0.0 - HTML Email",
        recipients=["recipient@example.com"],
        html=html_content,
        subtype="html"
    )
    
    await mail.send_message(message)
    return jsonify({"status": "HTML email sent!"})
```

### Bulk Email Support

```python
@app.post("/send-bulk")
async def send_bulk():
    email_data = (
        ("Subject 1", "Message 1", ["user1@example.com"]),
        ("Subject 2", "Message 2", ["user2@example.com"]),
        ("Subject 3", "Message 3", ["user3@example.com"]),
    )
    
    await mail.send_mass_mail(email_data)
    return jsonify({"status": "Bulk emails sent successfully!"})
```

## 📖 Documentation

For detailed documentation, examples, and API reference:
- **📄 [Documentation](https://marktennyson.github.io/flask-mailing)**
- **🔧 [Configuration Guide](https://marktennyson.github.io/flask-mailing/getting-started)**
- **📝 [Examples](https://marktennyson.github.io/flask-mailing/example/)**

## 🔄 Migration from v0.2.x

### Breaking Changes in v3.0.0
- **Minimum Python version**: 3.10+ (was 3.6+)
- **Minimum Flask version**: 3.1+ (was 2.0+)  
- **Pydantic v2**: Updated from v1.x to v2.11+
- **Email checking utilities**: Now optional dependencies

### Migration Steps
1. **Upgrade Python** to 3.10+ (recommended: 3.12+)
2. **Upgrade Flask** to 3.1+
3. **Update requirements.txt**:
   ```bash
   # Old
   flask-mailing>=0.2.3
   
   # New  
   flask-mailing>=3.0.0
   ```
4. **Test your application** - most APIs remain the same

## 📊 Version Compatibility

| Flask-Mailing | Python | Flask | Pydantic | Status |
|---------------|--------|-------|----------|---------|
| 3.0.0+ | 3.10-3.14 | 3.1+ | 2.11+ | ✅ Active |
| 0.2.x | 3.6+ | 2.0+ | 1.8+ | 🔒 Legacy |

## 🧪 Testing

```bash
# Run tests with Python 3.13
python -m pytest tests/ -v

# Run with multiple Python versions using tox
tox
```

## 🤝 Contributing 

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📋 Dependencies

### Core Dependencies
- `aiosmtplib>=4.0.1` - Async SMTP client
- `flask>=3.1.0` - Web framework
- `pydantic>=2.11.0` - Data validation
- `pydantic-settings>=2.9.0` - Settings management
- `email-validator>=2.3.0` - Email validation
- `jinja2>=3.1.6` - Template engine

### Optional Dependencies
- `redis>=5.3.0` - For email checking features
- `httpx>=0.28.1` - For HTTP-based email validation
- `dnspython>=2.8.0` - For DNS-based validation

## 📜 License

[MIT License](LICENSE)

## 📊 Stats

![Downloads](https://pepy.tech/badge/flask-mailing) ![Monthly Downloads](https://pepy.tech/badge/flask-mailing/month) ![Weekly Downloads](https://pepy.tech/badge/flask-mailing/week)

## 🔗 Links

- **🏠 [Github](https://github.com/marktennyson/flask-mailing)**
- **📄 [Documentation](https://marktennyson.github.io/flask-mailing)**  
- **🐍 [PyPI](https://pypi.org/project/flask-mailing)**
- **🐛 [Issues](https://github.com/marktennyson/flask-mailing/issues)**
- **💬 [Discussions](https://github.com/marktennyson/flask-mailing/discussions)**

---

**Made with ❤️ for the Python & Flask community**

*Flask-Mailing v3.0.0 - Ready for the future of Python development!*

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=marktennyson/flask-mailing&type=Date)](https://star-history.com/#marktennyson/flask-mailing&Date)

---

### Key Features :sparkles:

1. :arrows_counterclockwise: Supports asynchronous email sending using the built-in `asyncio` library in Python 3.10+.

2. :link: Easily integrates with Flask applications using the provided `Mail` extension.

3. :gear: Offers simple and intuitive configuration options for email providers such as SMTP, Sendgrid, and Mailgun.

4. :envelope: Supports HTML and plain-text message formats, as well as the option to send both formats in a multi-part message.

5. :paperclip: Provides support for file attachments in emails.

6. :art: Includes customizable email templates and support for Jinja2 templates.

7. :rocket: Offers a simple API for sending email messages, allowing for quick and easy implementation in any Flask project.

8. :email: Supports bulk email sending, allowing for the efficient delivery of messages to large email lists.

9. :bookmark_tabs: Provides options for customizing email headers and message priority levels.

10. :chart_with_upwards_trend: Supports email tracking through message IDs and delivery status notifications.

11. :microscope: Includes a comprehensive testing suite for ensuring the correct configuration and behavior of the email sending functionality.

12. :lock: Supports email encryption and authentication using TLS and SSL protocols.

13. :warning: Offers error handling and logging functionality for tracking and resolving email sending issues.

14. :book: Provides detailed documentation and active community support for resolving any issues or questions related to the package.

More information on [Getting-Started](https://marktennyson.github.io/flask-mailing/getting-started)

# 📥 Downloads
[![Downloads](https://pepy.tech/badge/flask-mailing)](https://pepy.tech/project/flask-mailing) [![Downloads](https://pepy.tech/badge/flask-mailing/month)](https://pepy.tech/project/flask-mailing) [![Downloads](https://pepy.tech/badge/flask-mailing/week)](https://pepy.tech/project/flask-mailing)
<br>

# 🚑 Package health score by [snyk.io](https://snyk.io)
[![Flask-Mailing](https://snyk.io/advisor/python/Flask-Mailing/badge.svg)](https://snyk.io/advisor/python/Flask-Mailing)

# 🔗 Important Links
#### ❤️ [Github](https://github.com/marktennyson/flask-mailing)    
#### 📄 [Documentation](https://marktennyson.github.io/flask-mailing)    
#### 🐍 [PYPI](https://pypi.org/project/flask-mailing)    

## 😀 Contributors ✨

Thanks go to these wonderful people ([🚧]):

<table>
<tr>
    <td align="center"><a href="https://github.com/marktennyson"><img src="https://avatars.githubusercontent.com/u/46404058?v=4" width="100px;" alt=""/><br /><sub><b>Aniket Sarkar</b></sub></a><br /><a href="#maintenance-tbenning" title="Answering Questions">💬</a> <a href="https://github.com/marktennyson/flask-mailing" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-jakebolam" title="Maintenance">🚧</a></td><br>
    <td align="center"><a href="https://github.com/jfkinslow"><img src="https://avatars.githubusercontent.com/u/4458739?v=4" width="100px;" alt=""/><br /><sub><b>Joshua Kinslow</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/agramfort"><img src="https://avatars.githubusercontent.com/u/161052?v=4" width="100px;" alt=""/><br /><sub><b>Alexandre Gramfort</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/ahmetkurukose"><img src="https://avatars.githubusercontent.com/u/1325263?v=4" width="100px;" alt=""/><br /><sub><b>
ahmetkurukose</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/Sriram-bb63"><img src="https://avatars.githubusercontent.com/u/71959217?v=4" width="100px;" alt=""/><br /><sub><b>
Sriram</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/CharlesTWood"><img src="https://avatars.githubusercontent.com/u/31315150?v=4" width="100px;" alt=""/><br/><sub><b>CharlesTWood</b></sub></a><br /></td>
</tr>
</table>

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!

Before you start please read [CONTRIBUTING](https://github.com/marktennyson/flask-mailing/blob/main/CONTRIBUTING.md)

# 📝 LICENSE

[MIT](https://raw.githubusercontent.com/marktennyson/flask-mailing/development/LICENSE)
