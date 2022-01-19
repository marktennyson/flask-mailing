"""
# ✉️ Flask-Mailing

Flask-Mailing adds SMTP mail sending to your Flask applications

Flask_Mail is dead now. This is the time to migrate a fully asynchronous 
based mailer library to send emails while using a Flask based application. 
Now Flask 2.0 supports the asynchronous view function then who is stopping you to use Flask-Mailing ?

The key features are:

-  Most of the Apis are very familiar with `Flask-Mail` module.
-  sending emails with either with Flask or using asyncio module 
-  sending files either from form-data or files from server
-  Using Jinja2 HTML Templates
-  email utils (utility allows you to check temporary email addresses, you can block any email or domain)
-  email utils has two available classes ```DefaultChecker``` and  ```WhoIsXmlApi```
-  Unittests using Mail

More information on [Getting-Started](https://marktennyson.github.io/flask-mailing/getting-started)

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

html = "<p>Thanks for using Flask-Mailing</p> "

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

# 📝 LICENSE

[MIT](LICENSE)
"""


from . import utils
from .config import ConnectionConfig
from .mail import Mail
from .schemas import Message as Message
from .schemas import MultipartSubtypeEnum as MultipartSubtypeEnum

version_info = (0, 1, 1)

__version__ = ".".join([str(v) for v in version_info])


__author__ = "aniketsarkar@yahoo.com"


__all__ = ["Mail", "ConnectionConfig", "Message", "utils", "MultipartSubtypeEnum"]
