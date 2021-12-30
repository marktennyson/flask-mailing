from dotenv import load_dotenv; load_dotenv()

from flask import jsonify
from base import create_app
from flask_mailing import Mail, Message

import os as os

mail = Mail()


"""
you can use mail.init_app() too.

mail.init_app(app)
"""

app = create_app()
mail.init_app(app)

@app.get('/')
def index():
    return jsonify(index=True)

#test email standart sending mail 
@app.get("/email")
async def simple_send() -> jsonify:

    message = Message(
        subject="Flask-Mailing module",
        recipients=[os.environ['MAIL_RECIPIENT']],
        body="This is the basic email body",
        )
    # message.add_recipient("aniforsana@gmail.com")

    
    await mail.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})


@app.get("/mail-file")
async def mail_file():
    message = Message(
        subject = "attachments based email",
        recipients = [os.environ['MAIL_RECIPIENT']],
        body = "This is the email body",
        attachments = ['attachments/attachment.txt']
    )
    with app.open_resource('attachments/test.html') as fp:
        message.attach("test.html", fp.read())

    await mail.send_message(message)
    return jsonify(message="email sent")

@app.get("/mail-html")
async def mail_html():
    
    message = Message(
        subject = "html template based email",
        recipients = [os.environ['MAIL_RECIPIENT']],
        template_body = {
                        "first_name": "Fred",
                        "last_name": "Fredsson"
                        }
        # attachments = ['attachments/attachment.txt']
    )
    await mail.send_message(message, template_name="test.html")
    return jsonify(message="email sent")

if __name__ == "__main__":
    app.run(debug=True)