# Getting Started

## 🕹 Guide

After installing the module and setting up your `Flask` app, you can start using Flask-Mailing.

### Main Classes and Packages

| Class | Description |
|-------|-------------|
| `Mail` | Main mail handler class |
| `Message` | Email message model with Pydantic validation |
| `ConnectionConfig` | Configuration class for mail settings |
| `MultipartSubtypeEnum` | MIME multipart subtypes |
| `RateLimiter` | Built-in rate limiting for email sending |
| `EmailSecurityValidator` | Security validation for emails |
| `utils.DefaultChecker` | Email checking utility |
| `utils.WhoIsXmlApi` | WhoIsXmlApi integration |

### Available Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| **MAIL_USERNAME** | Username for email authentication | - |
| **MAIL_PASSWORD** | Password for authentication | - |
| **MAIL_SERVER** | SMTP Mail server | - |
| **MAIL_PORT** | SMTP port (587 for TLS, 465 for SSL) | 587 |
| **MAIL_USE_TLS** | Enable TLS connection | False |
| **MAIL_USE_SSL** | Enable SSL connection | False |
| **MAIL_DEBUG** | Debug mode for mail sending | 0 |
| **MAIL_FROM** | Sender email address | - |
| **MAIL_DEFAULT_SENDER** | Default sender address | - |
| **MAIL_FROM_NAME** | Display name for sender | - |
| **TEMPLATE_FOLDER** | Jinja2 template folder path | None |
| **SUPPRESS_SEND** | Mock email sending (for testing) | 0 |
| **USE_CREDENTIALS** | Enable SMTP authentication | True |
| **VALIDATE_CERTS** | Verify mail server certificate | True |

### `Mail` Class

The main mail handler class with the following methods:

#### `send_message(message, template_name=None)`
Send a single email message.

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `Message` | The message object to send |
| `template_name` | `str \| None` | Jinja2 template name for HTML content |

```python
message = Message(
    subject="Hello",
    recipients=["user@example.com"],
    body="Hello World!"
)
await mail.send_message(message)
```

#### `send_mail(subject, message, recipients, **msgkwargs)`
Django-style email sending.

| Parameter | Type | Description |
|-----------|------|-------------|
| `subject` | `str` | Email subject |
| `message` | `str` | Email body |
| `recipients` | `list[str]` | List of recipient emails |
| `**msgkwargs` | `dict` | Additional Message parameters |

```python
await mail.send_mail(
    subject="Hello",
    message="Hello World!",
    recipients=["user@example.com"]
)
```

#### `send_mass_mail(datatuple)`
Send bulk emails efficiently.

| Parameter | Type | Description |
|-----------|------|-------------|
| `datatuple` | `tuple` | Tuple of (subject, message, recipients) tuples |

```python
emails = (
    ("Subject 1", "Message 1", ["user1@example.com"]),
    ("Subject 2", "Message 2", ["user2@example.com"]),
)
await mail.send_mass_mail(emails)
```


### `Message` Class

Pydantic v2 model for email messages with validation.

#### Attributes

| Attribute | Type | Description | Default |
|-----------|------|-------------|---------|
| `recipients` | `list[EmailStr]` | Primary recipients | Required |
| `subject` | `str` | Email subject | `""` |
| `body` | `str \| None` | Plain text body | `None` |
| `html` | `str \| None` | HTML body | `None` |
| `template_body` | `dict \| list \| None` | Template data | `None` |
| `template_params` | `dict \| list \| None` | Alternative template data | `None` |
| `attachments` | `list` | File attachments | `[]` |
| `cc` | `list[EmailStr]` | Carbon copy recipients | `[]` |
| `bcc` | `list[EmailStr]` | Blind carbon copy | `[]` |
| `reply_to` | `list[EmailStr]` | Reply-To addresses | `[]` |
| `charset` | `str` | Character encoding | `"utf-8"` |
| `subtype` | `str \| None` | Content subtype | `None` |
| `multipart_subtype` | `MultipartSubtypeEnum` | MIME multipart type | `mixed` |

#### Methods

- `add_recipient(recipient: str)` - Add another recipient
- `attach(filename, data, content_type, disposition, headers)` - Add attachment

   
### `utils.DefaultChecker` Class

Default class for checking email addresses from collected public resources.

!!! note "Optional Dependency"
    Requires `flask-mailing[email-checking]` to be installed.

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | `str \| None` | Optional source for email data |
| `db_provider` | `str \| None` | Switch to Redis backend |

```python
from flask_mailing.utils import DefaultChecker

checker = DefaultChecker()
await checker.fetch_temp_email_domains()

# Check if email is disposable
is_temp = await checker.is_dispasoble("test@tempmail.com")
```

### `utils.WhoIsXmlApi` Class

Integration with [WhoIsXmlApi](https://www.whoisxmlapi.com) for email verification.
Free tier: 1000 requests per month.

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | API access token |
| `email` | `str` | Email to verify |

```python
from flask_mailing.utils import WhoIsXmlApi

who_is = WhoIsXmlApi(token="your_token", email="test@example.com")
print(who_is.smtp_check_())      # Check SMTP server
print(who_is.is_dispasoble())    # Check if disposable
print(who_is.check_mx_record())  # Check MX records
print(who_is.free_check)         # Check if free email
```
