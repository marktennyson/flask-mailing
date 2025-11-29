from flask import Flask
import os as os


def create_app():
    app = Flask(__name__)

    app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
    app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
    # app.config['MAIL_FROM'] = "aniketsarkar1998@gmail.com"
    app.config["MAIL_PORT"] = os.environ["MAIL_PORT"]
    app.config["MAIL_SERVER"] = os.environ["MAIL_HOST"]
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["VALIDATE_CERTS"] = False
    # app.config['MAIL_TEMPLATE_FOLDER'] = Path(__file__).parent / 'attachments'

    return app
