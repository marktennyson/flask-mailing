"""
Flask-Mailing - Modern async email sending for Flask 3.1+

This file exists for backwards compatibility with older pip versions.
For new installations, pyproject.toml is the primary configuration.
"""

from setuptools import find_packages, setup

VERSION = (3, 0, 0)
AUTHOR = "Aniket Sarkar"
AUTHOR_EMAIL = "aniketsarkar@yahoo.com"


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="Flask-Mailing",
    version=".".join([str(i) for i in VERSION]),
    url="https://github.com/marktennyson/flask-mailing",
    license="MIT",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description="Modern Flask mail system for 2026+ with async support, bulk operations, and full Flask 3.1+ compatibility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "flask",
        "flask-mail",
        "flask-mailing",
        "async-flask",
        "asynchronous-email",
        "async-mailer",
        "flask-email",
        "smtp",
        "email",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "aiosmtplib>=4.0.2",
        "asgiref>=3.9.0",
        "blinker>=1.9.0",
        "pydantic>=2.11.0",
        "pydantic-settings>=2.9.0",
        "email-validator>=2.3.0",
        "typing-extensions>=4.14.0",
        "flask>=3.1.1",
        "jinja2>=3.1.6",
        "werkzeug>=3.1.3",
    ],
    extras_require={
        "email-checking": [
            "redis>=5.3.0",
            "httpx>=0.28.1",
            "dnspython>=2.8.0",
        ],
        "dev": [
            "pytest>=8.4.0",
            "pytest-asyncio>=1.0.0",
            "black>=25.1.0",
            "isort>=6.0.0",
            "mypy>=1.16.0",
            "ruff>=0.11.0",
            "coverage>=7.8.0",
            "pre-commit>=4.2.0",
        ],
        "docs": [
            "mkdocs>=1.6.0",
            "mkdocs-material>=9.6.0",
            "mkdocstrings>=0.29.0",
            "mkdocstrings-python>=1.16.0",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Email",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Typing :: Typed",
    ],
)
