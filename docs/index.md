# Flask-mailing

The flask-mailing simple lightweight mail system, sending emails and attachments(individual && bulk) fully asynchronously.

Flask_Mail is dead now. To use the mail service with your project you can use eaither [Flask-Mailing](https://github.com/marktennyson/flask-mailing) for legacy or [Flask-Mailman](https://github.com/waynerv/flask-mailman) for Django type implementation.

Flask-Mailing is a fork of `Sabuhi's` Fastapi-Mail package, providing similar functionality. 99% of the work was done by him, and the fork was made mainly provide the same features and the apis for the Flask Microframework.

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
    app.config['MAIL_TLS'] = True
    app.config['MAIL_SSL'] = False
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