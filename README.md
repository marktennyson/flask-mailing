# Flask-Mailing
Flask-Mailing adds SMTP mail sending to your Flask applications

Flask_Mail is dead now. To use the mail service with your project you can use eaither [Flask-Mailing](https://github.com/marktennyson/flask-mailing) for legacy or [Flask-Mailman](https://github.com/waynerv/flask-mailman) for Django type implementation.

Flask-Mailing is a fork of `Sabuhi's` Fastapi-Mail package, providing similar functionality. 99% of the work was done by him, and the fork was made mainly provide the same features and the apis for the Flask Microframework.

##### Need help to create and deploy the test cases.(Urgent)

###  🔨  Installation ###

```bash
 pip install flask-mailing
```
or install from source code
```bash
git clone https://github.com/marktennyson/flask-mailing.git && cd flask-mailing
python setup.py install
```

---
**Documentation**: [Flask-MAILING](https://marktennyson.github.io/flask-mailing)
---

The key features are:

-  sending emails with either with Flask or using asyncio module 
-  sending files either from form-data or files from server
-  Using Jinja2 HTML Templates
-  email utils (utility allows you to check temporary email addresses, you can block any email or domain)
-  email utils has two available classes ```DefaultChecker``` and  ```WhoIsXmlApi```
-  Unittests using Mail

More information on [Getting-Started](https://marktennyson.github.io/flask-mailing/getting-started)

### Guide


```python

from flask import Flask, jsonify
from flask_mailing import Mail, Message


app = Flask(__name__)

app.config['MAIL_USERNAME'] = "YourUserName"
app.config['MAIL_PASSWORD'] = "strong_password"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "your mail server"
app.config['MAIL_TLS'] = True
app.config['MAIL_SSL'] = False
app.config['USE_CREDENTIALS'] = True
app.config['VALIDATE_CERTS'] = True

mail = Mail(app)

html = """
<p>Thanks for using Flask-Mailing</p> 
"""


@app.post("/email")
async def simple_send() -> JSONResponse:

    message = Message(
        subject="Flask-Mailing module",
        recipients=["recipients@email-domain.com"],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    await mail.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})     
```

## List of Examples

For more examples of using flask-mailing please check [example](https://marktennyson.github.io/flask-mailing/flask-mailing/example/) section

# Contributing
Feel free to open issues and send pull requests.

## Contributors ✨

Thanks goes to these wonderful people ([🚧]):


<table>
<tr>
    <td align="center"><a href="https://github.com/marktennyson"><img src="https://avatars.githubusercontent.com/u/46404058?v=4" width="100px;" alt=""/><br /><sub><b>Aniket Sarkar</b></sub></a><br /><a href="#maintenance-tbenning" title="Answering Questions">💬</a> <a href="https://github.com/marktennyson/flask-mailing" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-jakebolam" title="Maintenance">🚧</a></td>
</tr>
</table>

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!

Before you start please read [CONTRIBUTING](https://github.com/marktennyson/flask-mailing/blob/master/CONTRIBUTING.md)



## LICENSE

[MIT](LICENSE)
