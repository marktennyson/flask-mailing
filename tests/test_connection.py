import os
import typing as t

import pytest as pt

from flask_mailing import Mail, Message

CONTENT = "file test content"

if t.TYPE_CHECKING is True:
    from flask import Flask


@pt.mark.asyncio
async def test_connection(app: "Flask"):
    message = Message(
        subject="test subject",
        recipients=["sabuhi.shukurov@gmail.com"],
        body="test",
        subtype="plain",
    )

    fm = Mail(app)

    await fm.send_message(message)

    assert message.body == "test"
    assert message.subtype == "plain"
    assert not message.template_body
    assert not message.html


@pt.mark.asyncio
async def test_html_message(app: "Flask"):
    sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
    subject = "testing"
    to = "to@example.com"
    msg = Message(subject=subject, recipients=[to], html="html test")
    fm = Mail(app)

    with fm.record_messages() as outbox:
        await fm.send_message(message=msg)

        assert len(outbox) == 1
        mail = outbox[0]
        assert mail["To"] == to
        assert mail["From"] == sender
        assert mail["Subject"] == subject
        assert not msg.subtype
    assert msg.html == "html test"


@pt.mark.asyncio
async def test_attachement_message(app: "Flask"):
    directory = os.getcwd()
    attachement = directory + "/files/attachement.txt"

    with open(attachement, "w") as file:
        file.write(CONTENT)

    subject = "testing"
    to = "to@example.com"
    msg = Message(
        subject=subject,
        recipients=[to],
        html="html test",
        subtype="html",
        attachments=[attachement],
    )
    fm = Mail(app)

    with fm.record_messages() as outbox:
        await fm.send_message(message=msg)
        mail = outbox[0]

        assert len(outbox) == 1
        assert mail._payload[1].get_content_maintype() == "application"
        assert (
            mail._payload[1].__dict__.get("_headers")[0][1]
            == "application/octet-stream"
        )


@pt.mark.asyncio
async def test_attachement_message_with_headers(app: "Flask"):
    directory = os.getcwd()
    attachement = directory + "/files/attachement.txt"

    with open(attachement, "w") as file:
        file.write(CONTENT)

    subject = "testing"
    to = "to@example.com"
    msg = Message(
        subject=subject,
        recipients=[to],
        html="html test",
        subtype="html",
        attachments=[
            {
                "file": attachement,
                "headers": {"Content-ID": "test ID"},
                "mime_type": "image",
                "mime_subtype": "png",
            }
        ],
    )
    fm = Mail(app)

    with fm.record_messages() as outbox:
        await fm.send_message(message=msg)

        assert len(outbox) == 1
        mail = outbox[0]
        assert mail._payload[1].get_content_maintype() == msg.attachments[0][1].get(
            "mime_type"
        )
        assert mail._payload[1].get_content_subtype() == msg.attachments[0][1].get(
            "mime_subtype"
        )

        assert mail._payload[1].__dict__.get("_headers")[0][1] == "image/png"
        assert mail._payload[1].__dict__.get("_headers")[4][1] == msg.attachments[0][
            1
        ].get("headers").get("Content-ID")


@pt.mark.asyncio
async def test_jinja_message_list(app: "Flask"):
    sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
    subject = "testing"
    to = "to@example.com"
    persons = [
        {"name": "Andrej"},
    ]
    msg = Message(subject=subject, recipients=[to], template_body=persons)
    fm = Mail(app)

    with fm.record_messages() as outbox:
        await fm.send_message(message=msg, template_name="email.html")

        assert len(outbox) == 1
        mail = outbox[0]
        assert mail["To"] == to
        assert mail["From"] == sender
        assert mail["Subject"] == subject
    assert msg.subtype == "html"
    assert msg.template_body == ("\n    \n    \n        Andrej\n    \n\n")


@pt.mark.asyncio
async def test_jinja_message_dict(app: "Flask"):
    sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
    subject = "testing"
    to = "to@example.com"
    person = {"name": "Andrej"}

    msg = Message(subject=subject, recipients=[to], template_body=person)
    fm = Mail(app)

    with fm.record_messages() as outbox:
        await fm.send_message(message=msg, template_name="email_dict.html")

        assert len(outbox) == 1
        mail = outbox[0]
        assert mail["To"] == to
        assert mail["From"] == sender
        assert mail["Subject"] == subject
    assert msg.subtype == "html"
    assert msg.template_body == ("\n   Andrej\n")


@pt.mark.asyncio
async def test_send_msg(app: "Flask"):
    msg = Message(subject="testing", recipients=["to@example.com"], body="html test")

    sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
    fm = Mail(app)
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        await fm.send_message(message=msg)

        assert len(outbox) == 1
        assert outbox[0]["subject"] == "testing"
        assert outbox[0]["from"] == sender
        assert outbox[0]["To"] == "to@example.com"


@pt.mark.asyncio
async def test_send_msg_with_subtype(app: "Flask"):
    msg = Message(
        subject="testing",
        recipients=["to@example.com"],
        body="<p html test </p>",
        subtype="html",
    )

    sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
    fm = Mail(app)
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        await fm.send_message(message=msg)

        assert len(outbox) == 1
        assert outbox[0]["subject"] == "testing"
        assert outbox[0]["from"] == sender
        assert outbox[0]["To"] == "to@example.com"
    assert msg.body == "<p html test </p>"
    assert msg.subtype == "html"


@pt.mark.asyncio
async def test_jinja_message_with_html(app: "Flask"):
    persons = [
        {"name": "Andrej"},
    ]

    msg = Message(
        subject="testing",
        recipients=["to@example.com"],
        template_body=persons,
        html="test html",
    )
    fm = Mail(app)

    with pt.raises(ValueError):
        await fm.send_message(message=msg, template_name="email.html")

    assert msg.template_body == ("\n    \n    \n        Andrej\n    \n\n")

    assert not msg.body
