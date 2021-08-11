from flask_mailing import __version__ as version
from flask_mailing import __author__ as author

from setuptools import setup,find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="Flask-Mailing",
    version=version,
    url="https://github.com/marktennyson/flask-mailing",
    license="MIT",
    author=author,
    author_email="aniketsarkar@yahoo.com",
    description="Flask mail system sending mails(individual, bulk) attachments(individual, bulk) fully asynchroniously",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flask", "django", "navycut", 'flask-mail', 'flask-mailing'],
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
    ],
    extras_require={},
    python_requires=">=3.6,<4",
    entry_points={
        "console_scripts":[
            "navycut=navycut.__main__:_main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
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