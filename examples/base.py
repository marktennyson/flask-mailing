from flask import Flask

def create_app():
    app = Flask(__name__)


    app.config['MAIL_USERNAME'] = "aniketsarkar1998@gmail.com"
    app.config['MAIL_PASSWORD'] = ""
    app.config['MAIL_FROM'] = "aniketsarkar1998@gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_TLS'] = True
    app.config['MAIL_SSL'] = False
    # app.config['MAIL_TEMPLATE_FOLDER'] = Path(__file__).parent / 'attachments'
    
    return app