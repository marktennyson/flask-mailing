# Flask-mailing

__Flask-Mailing__ is a highly efficient and user-friendly package that enables `Asynchronous` email messaging in Flask applications. Asynchronous email messaging is becoming increasingly popular because it allows applications to continue running while emails are being sent in the background. This makes it an ideal solution for time-sensitive applications that require a fast and responsive user experience.

With Flask-Mailing, developers can easily integrate asynchronous email messaging capabilities into their Flask applications without the need for complex configurations or additional dependencies. The package offers a variety of features, including support for multiple email providers, email templates, and error handling. It also supports common email protocols, such as `SMTP`, `SSL`, and `TLS`.

Moreover, Flask-Mailing offers a simple and intuitive API that allows developers to easily send emails in the background. It also provides advanced features, such as email tracking and reporting, which enable developers to monitor email performance and user engagement.

Whether you're building a small-scale application or a large-scale enterprise system, Flask-Mailing provides a reliable and scalable solution for Asynchronous email messaging in Flask applications.

Flask-Mail has been discontinued. However, you can still use email services with your Flask projects by using either Flask-Mailing for asynchronous implementation or Flask-Mailman for synchronous implementation.

- Flask-Mailing supports asynchronous email sending using the built-in `asyncio` library in Python 3.5+. It easily integrates with Flask applications using the provided `Mail` extension, offers simple and intuitive configuration options for email providers, supports HTML and plain-text message formats, and provides options for customizing email headers and message priority levels. It also includes customizable email templates, supports file attachments, and allows for bulk email sending, email tracking, encryption and authentication, error handling, and logging functionality.

- Flask-Mailman, on the other hand, provides a simple API for sending email messages synchronously, supports HTML and plain-text message formats, allows for customizing email headers and message priority levels, and provides options for email tracking and error handling. It also includes customizable email templates and supports file attachments.

Choose the package that best fits your project's requirements and start using email services with your Flask application!


Flask_Mail is dead now. To use the mail service with your project you can use eaither [Flask-Mailing](https://github.com/marktennyson/flask-mailing) for Asynchronous or [Flask-Mailman](https://github.com/waynerv/flask-mailman) for Synchronous implementation.

[![MIT licensed](https://img.shields.io/github/license/marktennyson/flask-mailing)](https://raw.githubusercontent.com/marktennyson/flask-mailing/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/network)
[![GitHub issues](https://img.shields.io/github/issues-raw/marktennyson/flask-mailing)](https://github.com/marktennyson/flask-mailing/issues)
[![Downloads](https://pepy.tech/badge/flask-mailing)](https://pepy.tech/project/flask-mailing)

## A Basic Demo for better understanding

```python

from flask import Flask, jsonify
from flask_mailing import Mail, Message

mail = Mail()

def create_app():
    app = Flask(__name__)


    app.config['MAIL_USERNAME'] = "your-email@your-domain.com"
    app.config['MAIL_PASSWORD'] = "world_top_secret_password"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_SERVER'] = "your-email-server.com"
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = "your-email@your-domain.com"
    mail.init_app(app)

    return app

#send a simple email using flask_mailing module.

app = create_app()

@app.get("/email")
async def simple_send():

    message = Message(
        subject="Flask-Mailing module",
        recipients=["aniketsarkar@yahoo.com"],
        body="This is the basic email body",
        )

    
    await mail.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})
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