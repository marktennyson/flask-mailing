from flask import Flask, jsonify
from flask_email import Mail, Message
from pathlib import Path

app = Flask(__name__)


app.config['MAIL_USERNAME'] = "aniketsarkar1998@gmail.com"
app.config['MAIL_PASSWORD'] = "zpaxrkdjaxgoqrll"
app.config['MAIL_FROM'] = "aniketsarkar1998@gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_TLS'] = True
app.config['MAIL_SSL'] = False
# app.config['MAIL_TEMPLATE_FOLDER'] = Path(__file__).parent / 'attachments'


fm = Mail(app)

#test email standart sending mail 
@app.get("/email")
async def simple_send() -> jsonify:

    message = Message(
        subject="Flask-Email module",
        recipients=["aniketsarkar@yahoo.com"],
        body="This is the basic email body",
        # subtype="html"
        )

    
    await fm.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})


@app.get("/mail-file")
async def mail_file():
    message = Message(
        subject = "attachments based email",
        recipients = ["aniketsarkar@yahoo.com"],
        body = "This is the email body",
        attachments = ['attachments/attachment.txt']
    )
    await fm.send_message(message)
    return jsonify(message="email sent")

@app.get("/mail-html")
async def mail_html():
    
    message = Message(
        subject = "html template based email",
        recipients = ["aniketsarkar@yahoo.com"],
        template_body = {
                        "first_name": "Fred",
                        "last_name": "Fredsson"
                        }
        # attachments = ['attachments/attachment.txt']
    )
    await fm.send_message(message, template_name="test.html")
    return jsonify(message="email sent")

if __name__ == "__main__":
    app.run(debug=True)