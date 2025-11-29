# Installation

## Requirements

- **Python 3.10+** (supports Python 3.10, 3.11, 3.12, 3.13, and 3.14)
- **Flask 3.1+**

## Using pip

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Flask-Mailing
pip install flask-mailing
```

## With Optional Dependencies

```bash
# With email checking utilities (Redis, DNS validation)
pip install flask-mailing[email-checking]

# Full development setup
pip install flask-mailing[dev,email-checking]
```

## Using source code

```bash
git clone https://github.com/marktennyson/flask-mailing && cd flask-mailing
pip install -e ".[dev,email-checking]"
```

## Core Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| aiosmtplib | ≥4.0.2 | Async SMTP client |
| flask | ≥3.1.0 | Web framework |
| pydantic | ≥2.11.0 | Data validation |
| pydantic-settings | ≥2.9.0 | Settings management |
| email-validator | ≥2.3.0 | Email validation |
| jinja2 | ≥3.1.6 | Template engine |

## Optional Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| redis | ≥5.3.0 | Email checking with Redis |
| httpx | ≥0.28.1 | HTTP-based email validation |
| dnspython | ≥2.8.0 | DNS-based validation |