# ✉️ Flask-Mailing
![Flask mail logo](https://github.com/marktennyson/flask-mailing/blob/main/logo/flask-mailing-logo-cropped.png?raw=true)

Flask-Mailing adds SMTP mail sending to your Flask applications

**Flask_Mail** is dead now. This is the time to migrate a fully asynchronous based mailer library to send emails while using a Flask based application. Now Flask 2.0 supports the asynchronous view function then who is stopping you to use __Flask-Mailing__ ?

__The key features are:__

-  Most of the Apis are very familiar with `Flask-Mail` module.
-  sending emails with either with Flask or using asyncio module 
-  sending files either from form-data or files from server
-  Using Jinja2 HTML Templates
-  email utils (utility allows you to check temporary email addresses, you can block any email or domain)
-  email utils has two available classes ```DefaultChecker``` and  ```WhoIsXmlApi```
-  Unittests using Mail

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
or install from source code
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

Thanks goes to these wonderful people ([🚧]):


<table>
<tr>
    <td align="center"><a href="https://github.com/marktennyson"><img src="https://avatars.githubusercontent.com/u/46404058?v=4" width="100px;" alt=""/><br /><sub><b>Aniket Sarkar</b></sub></a><br /><a href="#maintenance-tbenning" title="Answering Questions">💬</a> <a href="https://github.com/marktennyson/flask-mailing" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-jakebolam" title="Maintenance">🚧</a></td><br>
    <td align="center"><a href="https://github.com/jfkinslow"><img src="https://avatars.githubusercontent.com/u/4458739?v=4" width="100px;" alt=""/><br /><sub><b>Joshua Kinslow</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/agramfort"><img src="https://avatars.githubusercontent.com/u/161052?v=4" width="100px;" alt=""/><br /><sub><b>Alexandre Gramfort</b></sub></a><br /></td>
</tr>
</table>

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!

Before you start please read [CONTRIBUTING](https://github.com/marktennyson/flask-mailing/blob/main/CONTRIBUTING.md)



# 📝 LICENSE

[MIT](LICENSE)