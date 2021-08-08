import pytest
from flask_email.schemas import Message, MultipartSubtypeEnum
from flask_email.msg import MailMsg
import os

CONTENT = "file test content"


def test_initialize():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    assert message.subject == "test subject"


def test_recipients_properly_initialized():
    message = Message(
        subject="test subject",
        recipients=[],
        body="test",
        subtype="plain"
    )

    assert message.recipients == []


def test_sendto_properly_set():
    msg = Message(subject="subject", recipients=["somebody@here.com", "somebody2@here.com"],
                        cc=["cc@example.com"], bcc=["bcc@example.com"], reply_to=["replyto@example.com"])

    assert len(msg.recipients) == 2
    assert len(msg.cc) == 1
    assert len(msg.bcc) == 1
    assert len(msg.reply_to) == 1




def test_plain_message():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    assert message.body == "test"



def test_charset():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    assert message.charset == "utf-8"

def test_message_str():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    assert type(message.body) == str


def test_plain_message_with_attachments():
    directory = os.getcwd()
    attachement  = directory + "/files/attachement.txt"
 
    msg = Message(subject="testing",
                        recipients=["to@example.com"],
                        attachments=[attachement],
                        body="test mail body")
    
    with open(attachement, "w") as file:
        file.write(CONTENT)

    assert len(msg.attachments) == 1




def test_empty_subject_header():
    message = Message(
        subject="",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    assert len(message.subject) == 0


def test_bcc():
    msg = Message(subject="subject", recipients=[],
                        bcc=["bcc@example.com"])

    assert len(msg.bcc) == 1
    assert msg.bcc == ["bcc@example.com"]

def test_replyto():
    msg = Message(subject="subject", recipients=[],
                        reply_to=["replyto@example.com"])

    assert len(msg.reply_to) == 1
    assert msg.reply_to == ["replyto@example.com"]

def test_cc():
    msg = Message(subject="subject", recipients=[],
                        cc=["cc@example.com"])

    assert len(msg.cc) == 1
    assert msg.cc == ["cc@example.com"]


def test_multipart_subtype():
    message = Message(
        subject="test subject",
        recipients=["to@example.com"],
        body="test",
        subtype="plain"
    )
    assert  message.multipart_subtype == MultipartSubtypeEnum.mixed


@pytest.mark.asyncio
async def test_msgid_header():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    msg = MailMsg(**message.dict())
    msg_object = await msg._message('test@example.com')
    assert msg_object['Message-ID'] is not None


@pytest.mark.asyncio
async def test_message_charset():
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain"
    )

    msg = MailMsg(**message.dict())
    msg_object = await msg._message('test@example.com')
    assert msg_object._charset is not None
    assert msg_object._charset == "utf-8"