# Examples

## Sending Emails with Flask-Mailing v3.0.0

This guide covers common email sending patterns with Flask-Mailing.

## Basic Configuration

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

# Using application factory pattern
def create_app():
    app = Flask(__name__)
    app.config.update(...)
    mail.init_app(app)
    return app

@app.post("/send-email")
async def simple_send():
    message = Message(
        subject="Flask-Mailing v3.0.0",
        recipients=["recipient@example.com"],
        body="Hello from Flask-Mailing!",
        subtype="plain"
    )
    
    await mail.send_message(message)
    return jsonify({"message": "Email sent successfully!"})
```

#### Add recipient using `add_recipient` method

```python
message.add_recipient("another@example.com")
```


## Send HTML Email

```python
@app.post("/html-email")
async def html_email():
    html_content = """
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h1 style="color: #2c3e50;">Hello! 👋</h1>
            <p>This is an HTML email from Flask-Mailing v3.0.0</p>
        </body>
    </html>
    """
    
    message = Message(
        subject="Flask-Mailing HTML Email",
        recipients=["recipient@example.com"],
        html=html_content,
        subtype="html"
    )
    
    await mail.send_message(message)
    return jsonify({"message": "HTML email sent!"})
```

## Sending Files

```python
@app.post("/email-with-file")
async def mail_file():
    message = Message(
        subject="Email with Attachment",
        recipients=["recipient@example.com"],
        body="Please find the attached file.",
        attachments=["attachments/document.pdf"]
    )
    await mail.send_message(message)
    return jsonify({"message": "Email with attachment sent!"})
```

### Using `attach` method

```python
with open("attachments/example.txt", "rb") as fp:
    message.attach("example.txt", fp.read())
```

## Using Jinja2 HTML Templates

Enable Jinja2 template emails by setting `TEMPLATE_FOLDER` or use the app's default template folder:

```python
from pathlib import Path

# Optional: Set custom template folder
app.config["TEMPLATE_FOLDER"] = Path(__file__).parent / 'email-templates'

@app.post("/email-with-template")
async def mail_html():
    message = Message(
        subject="Welcome Email",
        recipients=["recipient@example.com"],
        template_body={
            "first_name": "John",
            "last_name": "Doe"
        }
    )
    # Or use template_params (same effect)
    message = Message(
        subject="Welcome Email",
        recipients=["recipient@example.com"],
        template_params={
            "first_name": "John",
            "last_name": "Doe"
        }
    )

    await mail.send_message(message, template_name="welcome.html")
    return jsonify({"message": "Template email sent!"})
```

### Template Example

In your Jinja2 template (`welcome.html`):

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Hello, {{ first_name }} {{ last_name }}!</h1>
    <p>Welcome to our service.</p>
</body>
</html>
```

## Customizing Attachments with Headers and MIME Type

Add custom headers and MIME types for attachments (e.g., inline images):

```python
message = Message(
    subject="Email with Inline Image",
    recipients=["recipient@example.com"],
    html="<img src='cid:logo_image'>",
    subtype="html",
    attachments=[
        {
            "file": "/path/to/logo.png",
            "headers": {"Content-ID": "<logo_image>"},
            "mime_type": "image",
            "mime_subtype": "png",
        }
    ],
)

await mail.send_message(message)
```

## Email Utilities

!!! note "Optional Dependency"
    Requires `pip install flask-mailing[email-checking]`

The utility allows you to check temporary/disposable email addresses and block emails or domains.

### Check Disposable Email

```python
from flask_mailing.utils import DefaultChecker

async def get_checker():
    checker = DefaultChecker()
    await checker.fetch_temp_email_domains()
    return checker

@app.post("/check-email")
async def check_email():
    email = "test@tempmail.com"
    checker = await get_checker()
    
    if await checker.is_dispasoble(email):
        return jsonify({"error": "Disposable emails not allowed"}), 400
    
    return jsonify({"message": "Email is valid"})
```

### Add Disposable Domain

```python
@app.post("/add-disposable")
async def add_disp_domain():
    domains = ["tempmail.com", "throwaway.com"]
    checker = await get_checker()
    result = await checker.add_temp_domain(domains)
    return jsonify({"result": result})
```

### Block Domain

```python
@app.post("/block-domain")
async def block_domain():
    domain = "spam-domain.com"
    checker = await get_checker()
    await checker.blacklist_add_domain(domain)
    return jsonify({"message": f"{domain} added to blacklist"})
```

### Check if Domain is Blocked

```python
@app.post("/check-domain")
async def check_blocked_domain():
    domain = "spam-domain.com"
    checker = await get_checker()
    is_blocked = await checker.is_blocked_domain(domain)
    return jsonify({"blocked": is_blocked})
```

### Block Email Address

```python
@app.post("/block-email")
async def block_email():
    email = "spammer@example.com"
    checker = await get_checker()
    await checker.blacklist_add_email(email)
    return jsonify({"message": f"{email} blocked"})
```

### Check MX Record

```python
@app.post("/check-mx")
async def check_mx():
    domain = "gmail.com"
    checker = await get_checker()
    has_mx = await checker.check_mx_record(domain)
    return jsonify({"has_mx_record": has_mx})
```

### WhoIsXmlApi Integration

```python
from flask_mailing.utils import WhoIsXmlApi

who_is = WhoIsXmlApi(token="your_api_token", email="test@example.com")

print(who_is.smtp_check_())      # Check SMTP server
print(who_is.is_dispasoble())    # Check if disposable
print(who_is.check_mx_record())  # Check MX records
print(who_is.free_check)         # Check if free email provider
```
