from flask import Flask, jsonify
from flask_email import Mail, Message

app = Flask(__name__)


app.config['MAIL_USERNAME'] = "aniketsarkar1998@gmail.com"
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_FROM'] = "aniketsarkar1998@gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_TLS'] = True
app.config['MAIL_SSL'] = False


#test email standart sending mail 
@app.get("/email")
async def simple_send() -> jsonify:

    message = Message(
        subject="Flask-Email module",
        recipients=["aniketsarkar@yahoo.com"],
        body="This is the basic email body",
        # subtype="html"
        )

    fm = Mail(app)
    await fm.send_message(message)
    return jsonify(status_code=200, content={"message": "email has been sent"})

if __name__ == "__main__":
    app.run(debug=True)