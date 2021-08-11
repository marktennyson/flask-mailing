# Flask-mail

The flask-mailing simple lightweight mail system, sending emails and attachments(individual && bulk)


<!-- [![MIT licensed](https://img.shields.io/github/license/marktennyson/flask-mailing)](https://raw.githubusercontent.com/marktennyson/flask-mailing/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/marktennyson/flask-mailing.svg)](https://github.com/marktennyson/flask-mailing/network)
[![GitHub issues](https://img.shields.io/github/issues-raw/marktennyson/flask-mailing)](https://github.com/marktennyson/flask-mailing/issues) -->
[![Downloads](https://pepy.tech/badge/flask-mailing)](https://pepy.tech/project/flask-mailing)



## Using Jinja2 HTML Templates

In order to use Jinja template langauge, your must specify email folder within your applications working directory.

In sending HTML emails, the CSS expected by mail servers -outlook, google, etc- must be inline CSS. Flask mail passes _"body"_ to the rendered template. In creating the template for emails the dynamic objects should be used with the assumption that the variable is named "_body_" and that it is a python dict.

check out jinja2 for more details 
[jinja2](https://jinja.palletsprojects.com/en/2.11.x/)



##  Guide for Email Utils

The utility allows you to check temporary email addresses, you can block any email or domain. 
You can connect Redis to save and check email addresses. If you do not provide a Redis configuration, 
then the utility will save it in the list or set by default.



## Writing unittests using Flask-Mail
Flask mails allows you to write unittest for your application without sending emails to
non existent email address by mocking the email to be sent. To mock sending out mails, set
the suppress configuraton to true. Suppress send defaults to False to prevent mocking within applications.


## Support for Reply-To header is added
Use this just like bcc but to specify addresses that should receive a reply to your message. E-mail systems MAY respect this as per RFC 2822.