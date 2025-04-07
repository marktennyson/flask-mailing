# Example

## Sending emails using Flask-Mailing

## List of Examples 

### Basic configuration

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

#### Add recipient using `add_recipient` method

```python
message.add_recipient("recipient@emldomain.com")
```


### Send a simple html message
```python

html = """
<p>Hi this test mail, thanks for using Flask-Mailing</p> 
"""

@app.get("/html-email")
async def html_email():

    message = Message(
        subject="Flask-Mailing module test html mail",
        recipients=["aniketsarkar@yahoo.com"],
        html=html,
        subtype="html"
        )

    
    await mail.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})
```

### Sending files

```python
@app.get("/mail-file")
async def mail_file():
    message = Message(
        subject = "attachments based email",
        recipients = ["aniketsarkar@yahoo.com"],
        body = "email with attachments, email body.",
        attachments = ['attachments/attachment.txt']
    )
    await mail.send_message(message)
    return jsonify(message="email sent")
```
#### Sending files using `attach` method
```python
with app.open_resource("attachments/example.txt") as fp:
    message.attach("example.txt", fp.read())
```

### Using Jinja2 HTML Templates

You can enable Jinja2 HTML Template emails by setting the `TEMPLATE_FOLDER` configuration option, and supplying a value (which is just the name of the template file within the `TEMPLATE_FOLDER` dir) for the `template_name` parameter in `Mail.send_message()`. You then can pass a Dict as the `template_body` property of your `Message` object. If you haven't provided the `TEMPLATE_FOLDER` configuration option, then the module will take the app's jinja2 environment for templating and you can use templates from app's default template folder:

```python
from pathlib import Path

app.config["TEMPLATE_FOLDER"] = Path(__file__).parent / 'email-templates'
"""
Don't use this configuration if you want to use the default jinja2 environment.
"""
@app.get("/mail-html")
async def mail_html():
    
    message = Message(
        subject = "html template based email",
        recipients = ["aniketsarkar@yahoo.com"],
        template_body = {
                        "first_name": "Hare",
                        "last_name": "Krishna"
                        }
        # attachments = ['attachments/attachment.txt']
    )
    #or
    message = Message(
        subject = "html template based email",
        recipients = ["aniketsarkar@yahoo.com"],
        template_params = {
                        "first_name": "Hare",
                        "last_name": "Krishna"
                        }
        # attachments = ['attachments/attachment.txt']
    )

    await mail.send_message(message, template_name="test.html")
    return jsonify(message="email sent")
```
For example, assume we pass a `template_body` of:
```python
{
  "first_name": "Hare",
  "last_name": "Krishna"
}
```
We can reference the variables in our Jinja templates as per normal:
```html
...
<span>Hello, {{ first_name }}!</span>
...
```
#### Legacy Behaviour

The original behaviour was to wrap the Dict you provide in a variable named `body` when it was provided to 
Jinja behind the scenes. In these versions, you can then access your dict in your template like so:


```
...
<span>Hello,  body.first_name !</span>
...
```


As you can see our keys in our dict are no longer the top level, they are part of the `body` variable. Nesting works 
as per normal below this level also. 

### Customizing attachments by headers and MIME type

Used for example for referencing Content-ID images in html of email

```python
message = Message(
    subject='Flask-Mailing module',
    recipients=recipients,
    html="<img src='cid:logo_image'>",
    subtype='html',
    attachments=[
            {
                "file": "/path/to/file.png"),
                "headers": {"Content-ID": "<logo_image>"},
                "mime_type": "image",
                "mime_subtype": "png",
            }
        ],
)

await mail.send_message(message)
```

##  Guide for email utils

The utility allows you to check temporary email addresses, you can block any email or domain. 
You can connect Redis to save and check email addresses. If you do not provide a Redis configuration, 
then the utility will save it in the list or set by default.

### Check dispasoble email address
```python
async def default_checker():
    checker = DefaultChecker()  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains() # require to fetch temporary email domains
    return checker

@app.get('/email/dispasoble')
async def simple_send():
    domain = "gmail.com, 
    checker = await default_checker()
    if await checker.is_dispasoble(domain):
        return jsonify(status_code=400, content={'message': 'this is dispasoble domain'})

    return jsonify(status_code=200, content={'message': 'email has been sent'})
```

### Add dispasoble email address

```python
@app.get('/email/dispasoble')
async def add_disp_domain():
    domains: list = ["gmail.com"]
    checker: DefaultChecker = await default_checker()

    res = await checker.add_temp_domain(domains)

    return jsonify(status_code=200, content={'result': res})
```
### Add domain to blocked list

```python
@app.get('/email/blocked/domains')
async def block_domain():
    domain: str = "gmail.com"
    checker: DefaultChecker = await default_checker()

    await checker.blacklist_add_domain(domain)

    return jsonify(status_code=200, content={'message': f'{domain} added to blacklist'})
```
### Check domain blocked or not

```python
@app.get('/email/blocked/check-domains')
async def get_blocked_domain():
    domain: str ='gmail.com'
    checker: DefaultChecker = await default_checker()
    res = await checker.is_blocked_domain(domain)

    return jsonify(status_code=200, content={"result": res})
```

### Add email address to blocked list

```python
@app.get('/email/blocked/address')
async def block_address():
    email: str ='hacker@gmail.com'
    checker: DefaultChecker = await default_checker()
    await checker.blacklist_add_email(email)

    return jsonify(status_code=200, content={"result": True})
```

### Check email blocked or not

```python
@app.get('/email/blocked/address')
async def get_block_address():
    email: str ='hacker@gmail.com'
    checker: DefaultChecker = await default_checker()
    res = await checker.is_blocked_address(email)

    return jsonify(status_code=200, content={"result": res})
```

### Check MX record

```python
@app.get("/email/check-mx")
async def check_mx_record():
    checker = await default_checker()
    domain = "gmail.com"
    res = await checker.check_mx_record(domain, False)
    
    return jsonify(status_code=200, content={'result': res})
```

### Remove email address from blocked list
```python
@app.get('/email/blocked/address')
async def del_blocked_address():
    checker = await default_checker()
    email = "hacker@gmail.com"
    res = await checker.blacklist_rm_email(email)

    return jsonify(status_code=200, content={"result": res})
```

### Remove domain from blocked list

```python
@app.get('/email/blocked/domains')
async def del_blocked_domain():
    checker = await default_checker()
    domain = "gmail.com"
    res = await checker.blacklist_rm_domain(domain)

    return jsonify(status_code=200, content={"result": res})
```

### Remove domain from temporary list

```python
@app.get('/email/dispasoblee')
async def del_disp_domain():
    checker = await default_checker()
    domains = ["gmail.com"]
    res = await checker.blacklist_rm_temp(domains)

    return jsonify(status_code=200, content={'result': res})
```

###  WhoIsXmlApi
```python
from flask_mailing.utils import WhoIsXmlApi

who_is = WhoIsXmlApi(token="Your access token", email="your@mailaddress.com")

print(who_is.smtp_check_())    #check smtp server
print(who_is.is_dispasoble()) # check email is disposable or not
print(who_is.check_mx_record()) # check domain mx records 
print(who_is.free_check) # check email domain is free or not

```
