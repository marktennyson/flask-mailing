from setuptools import (
    setup,
    find_packages
    )

VERSION = (0, 1, 1)
AUTHOR = "Aniket Sarkar"
AUTHOR_EMAIL = "aniketsarkar@yahoo.com"


with open("README.md", "r") as f:
    long_description = f.read()
    pass


setup(
    name="Flask-Mailing",
    version=".".join([str(i) for i in list(VERSION)]),
    url="https://github.com/marktennyson/flask-mailing",
    license="MIT",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description="Flask mail system sending mails(individual, bulk) attachments(individual, bulk) fully asynchroniously",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "flask",
        'flask-mail',
        'flask-mailing',
        'async-flask',
        'asynchroniously-send-email-in-flask',
        'async-mailer',
        'flask-email',
        'flask-mailman'
        ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "aiosmtplib>=1.1.6",
        "aioredis>=2.0.0",
        "asgiref>=3.4.1",
        "blinker>=1.4",
        "pydantic>=1.8.2",
        "email-validator>=1.1.3",
        "typing-extensions>=3.10.0.0",
        "httpx>=0.21.3",
        "flask>=2.0.0"
    ],
    extras_require={},
    python_requires=">=3.6,<4",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
