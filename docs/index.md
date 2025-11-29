# Flask-Mailing v3.0.0 🚀

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.1+](https://img.shields.io/badge/flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![Pydantic v2.11+](https://img.shields.io/badge/pydantic-2.11+-red.svg)](https://pydantic.dev/)

**Flask-Mailing** is a highly efficient and user-friendly package that enables `Asynchronous` email messaging in Flask applications. Built for **2026 and beyond**, it combines cutting-edge Python 3.10+ features, Flask 3.1+ compatibility, and enterprise-grade security.

## ✨ What's New in v3.0.0

- **🐍 Python 3.10-3.14 Support** - Modern union syntax (`str | None`) and built-in generics
- **⚡ Flask 3.1+ Compatibility** - Full async support with latest Flask
- **📦 Pydantic v2.11+** - Latest validation with enhanced performance
- **🔒 Enhanced Security** - Rate limiting, email validation, path traversal protection
- **🏗️ Modern Build System** - Ruff, Black, isort, mypy integration
- **🧪 Comprehensive Testing** - Full test coverage with pytest-asyncio

## Why Flask-Mailing?

Asynchronous email messaging allows applications to continue running while emails are being sent in the background. This makes it ideal for time-sensitive applications requiring a fast and responsive user experience.

With Flask-Mailing, developers can easily integrate asynchronous email messaging capabilities into their Flask applications without complex configurations. The package offers:

- Support for multiple email providers
- Email templates with Jinja2
- Comprehensive error handling
- Common email protocols (`SMTP`, `SSL`, `TLS`)
- Advanced features like email tracking and reporting

Whether you're building a small-scale application or a large-scale enterprise system, Flask-Mailing provides a reliable and scalable solution.

## Flask-Mailing vs Flask-Mailman

Flask-Mail has been discontinued. Choose between:

- **Flask-Mailing** (this package) - Asynchronous email with Python 3.10+ and Flask 3.1+ support
- **Flask-Mailman** - Synchronous email implementation


[![MIT licensed](https://img.shields.io/github/license/marktennyson/flask-mailing)](https://raw.githubusercontent.com/marktennyson/flask-mailing/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/network)
[![GitHub issues](https://img.shields.io/github/issues-raw/marktennyson/flask-mailing)](https://github.com/marktennyson/flask-mailing/issues)
[![Downloads](https://pepy.tech/badge/flask-mailing)](https://pepy.tech/project/flask-mailing)

## 📋 Requirements

- **Python 3.10+** (3.14 compatible!)
- **Flask 3.1+** with async support

## Quick Start

```python
from flask import Flask, jsonify
from flask_mailing import Mail, Message

app = Flask(__name__)

# Modern Flask 3.1+ configuration
app.config.update(
    MAIL_USERNAME="your-email@your-domain.com",
    MAIL_PASSWORD="your_app_password",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_DEFAULT_SENDER="your-email@your-domain.com",
    MAIL_FROM_NAME="Your App Name"
)

mail = Mail(app)

@app.post("/send-email")
async def send_email():
    message = Message(
        subject="Flask-Mailing v3.0.0 Test",
        recipients=["recipient@example.com"],
        body="Hello from Flask-Mailing v3.0.0! 🚀",
        subtype="plain"
    )
    
    await mail.send_message(message)
    return jsonify({"status": "Email sent successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
```

## Using Jinja2 HTML Templates

In order to use Jinja template langauge, your must specify email folder within your applications working directory.

In sending HTML emails, the CSS expected by mail servers -outlook, google, etc- must be inline CSS. Flask mail passes _"body"_ to the rendered template. In creating the template for emails the dynamic objects should be used with the assumption that the variable is named "_body_" and that it is a python dict.

check out jinja2 for more details 
[jinja2](https://jinja.palletsprojects.com/en/2.11.x/)



##  Guide for Email Utils

The utility allows you to check temporary email addresses, you can block any email or domain. 
You can connect Redis to save and check email addresses. If you do not provide a Redis configuration, 
then the utility will save it in the list or set by default.



## Writing unittests using Flask-Mailing
Flask mails allows you to write unittest for your application without sending emails to
non existent email address by mocking the email to be sent. To mock sending out mails, set
the suppress configuraton to true. Suppress send defaults to False to prevent mocking within applications.


## Support for Reply-To header is added
Use this just like bcc but to specify addresses that should receive a reply to your message. E-mail systems MAY respect this as per RFC 2822.