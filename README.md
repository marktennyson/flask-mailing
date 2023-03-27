# ✉️ Flask-Mailing
![Flask mail logo](https://github.com/marktennyson/flask-mailing/blob/main/logo/flask-mailing-logo-cropped.png?raw=true)

__Flask-Mailing__ is a highly efficient and user-friendly package that enables `Asynchronous` email messaging in Flask applications. Asynchronous email messaging is becoming increasingly popular because it allows applications to continue running while emails are being sent in the background. This makes it an ideal solution for time-sensitive applications that require a fast and responsive user experience.

With Flask-Mailing, developers can easily integrate asynchronous email messaging capabilities into their Flask applications without the need for complex configurations or additional dependencies. The package offers a variety of features, including support for multiple email providers, email templates, and error handling. It also supports common email protocols, such as `SMTP`, `SSL`, and `TLS`.

Moreover, Flask-Mailing offers a simple and intuitive API that allows developers to easily send emails in the background. It also provides advanced features, such as email tracking and reporting, which enable developers to monitor email performance and user engagement.

Whether you're building a small-scale application or a large-scale enterprise system, Flask-Mailing provides a reliable and scalable solution for Asynchronous email messaging in Flask applications.


### Key Features :sparkles:

1. :arrows_counterclockwise: Supports asynchronous email sending using the built-in `asyncio` library in Python 3.5+.

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

# 🔨 Installation ###

```bash
 pip install flask-mailing
```
or install from the source code
```bash
git clone https://github.com/marktennyson/flask-mailing.git && cd flask-mailing
python -m pip install .
```

# 🦮 Guide


```python

from flask import Flask, jsonify
from flask_mailing import Mail, Message

app = Flask(__name__)

app.config['MAIL_USERNAME'] = "YourUserName"
app.config['MAIL_PASSWORD'] = "strong_password"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "your mail server"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['USE_CREDENTIALS'] = True
app.config['VALIDATE_CERTS'] = True
app.config['MAIL_DEFAULT_SENDER'] = "youremailid@doaminname.com"

mail = Mail(app)

html = """
<p>Thanks for using Flask-Mailing</p> 
"""


@app.post("/email")
async def simple_send():
    message = Message(
        subject="Flask-Mailing module",
        recipients=["recipients@email-domain.com"],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )
    await mail.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})     
```

# 🪜 List of Examples

For more examples of using flask-mailing please check [example](https://marktennyson.github.io/flask-mailing/example/) section

# 👍 Contributing
Feel free to open issues and send pull requests.

## 😀 Contributors ✨

Thanks go to these wonderful people ([🚧]):


<table>
<tr>
    <td align="center"><a href="https://github.com/marktennyson"><img src="https://avatars.githubusercontent.com/u/46404058?v=4" width="100px;" alt=""/><br /><sub><b>Aniket Sarkar</b></sub></a><br /><a href="#maintenance-tbenning" title="Answering Questions">💬</a> <a href="https://github.com/marktennyson/flask-mailing" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-jakebolam" title="Maintenance">🚧</a></td><br>
    <td align="center"><a href="https://github.com/jfkinslow"><img src="https://avatars.githubusercontent.com/u/4458739?v=4" width="100px;" alt=""/><br /><sub><b>Joshua Kinslow</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/agramfort"><img src="https://avatars.githubusercontent.com/u/161052?v=4" width="100px;" alt=""/><br /><sub><b>Alexandre Gramfort</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/ahmetkurukose"><img src="https://avatars.githubusercontent.com/u/1325263?v=4" width="100px;" alt=""/><br /><sub><b>
ahmetkurukose</b></sub></a><br /></td>
</tr>
</table>

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!

Before you start please read [CONTRIBUTING](https://github.com/marktennyson/flask-mailing/blob/main/CONTRIBUTING.md)



# 📝 LICENSE

[MIT](https://raw.githubusercontent.com/marktennyson/flask-mailing/development/LICENSE)
