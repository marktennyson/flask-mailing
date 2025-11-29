"""
Flask-Mailing v3.0.0 - Message Tests
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from flask_mailing.msg import MailMsg
from flask_mailing.schemas import Message, MultipartSubtypeEnum

CONTENT = "file test content"


def test_initialize() -> None:
    """Test Message initialization."""
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    assert message.subject == "test subject"


def test_recipients_properly_initialized() -> None:
    """Test empty recipients list."""
    message = Message(
        subject="test subject",
        recipients=[],
        body="test",
        subtype="plain",
    )

    assert message.recipients == []


def test_add_recipient_method() -> None:
    """Test add_recipient method."""
    message = Message(
        subject="test subject",
        recipients=[],
        body="test",
        subtype="plain",
    )
    message.add_recipient("aniketsarkar@yahoo.com")

    assert message.recipients == ["aniketsarkar@yahoo.com"]


def test_sendto_properly_set() -> None:
    """Test multiple recipient fields."""
    msg = Message(
        subject="subject",
        recipients=["somebody@here.com", "somebody2@here.com"],
        cc=["cc@example.com"],
        bcc=["bcc@example.com"],
        reply_to=["replyto@example.com"],
    )

    assert len(msg.recipients) == 2
    assert len(msg.cc) == 1
    assert len(msg.bcc) == 1
    assert len(msg.reply_to) == 1


def test_plain_message() -> None:
    """Test plain text message body."""
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    assert message.body == "test"


def test_charset() -> None:
    """Test default charset."""
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    assert message.charset == "utf-8"


def test_message_str() -> None:
    """Test message body is string."""
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    assert isinstance(message.body, str)


def test_plain_message_with_attachments() -> None:
    """Test message with file attachment."""
    directory = os.getcwd()
    attachment = directory + "/files/attachement.txt"

    with open(attachment, "w") as file:
        file.write(CONTENT)

    msg = Message(
        subject="testing",
        recipients=["to@example.com"],
        attachments=[attachment],
        body="test mail body",
    )

    assert len(msg.attachments) == 1


def test_plain_message_with_attach_method() -> None:
    """Test message attach method."""
    directory = os.getcwd()
    attachment = directory + "/files/attachement_1.txt"

    msg = Message(
        subject="testing",
        recipients=["to@example.com"],
        body="test mail body",
    )

    with open(attachment, "w") as file:
        file.write(CONTENT)

    with open(attachment, "rb") as fp:
        msg.attach("attachement_1.txt", fp.read())

    assert len(msg.attachments) == 1


def test_empty_subject_header() -> None:
    """Test empty subject."""
    message = Message(
        subject="",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    assert len(message.subject) == 0


def test_bcc() -> None:
    """Test BCC field."""
    msg = Message(
        subject="subject",
        recipients=[],
        bcc=["bcc@example.com"],
    )

    assert len(msg.bcc) == 1
    assert msg.bcc == ["bcc@example.com"]


def test_replyto() -> None:
    """Test Reply-To field."""
    msg = Message(
        subject="subject",
        recipients=[],
        reply_to=["replyto@example.com"],
    )

    assert len(msg.reply_to) == 1
    assert msg.reply_to == ["replyto@example.com"]


def test_cc() -> None:
    """Test CC field."""
    msg = Message(
        subject="subject",
        recipients=[],
        cc=["cc@example.com"],
    )

    assert len(msg.cc) == 1
    assert msg.cc == ["cc@example.com"]


def test_multipart_subtype() -> None:
    """Test default multipart subtype."""
    message = Message(
        subject="test subject",
        recipients=["to@example.com"],
        body="test",
        subtype="plain",
    )
    assert message.multipart_subtype == MultipartSubtypeEnum.mixed


@pytest.mark.asyncio
async def test_msgid_header() -> None:
    """Test Message-ID header generation."""
    message = Message(
        subject="test subject",
        recipients=["sp001@gmail.com"],
        body="test",
        subtype="plain",
    )

    msg = MailMsg(**message.model_dump())
    msg_object = await msg._message("test@example.com")
    assert msg_object["Message-ID"] is not None


@pytest.mark.asyncio
async def test_message_charset() -> None:
    """Test message charset in MIME."""
    message = Message(
        subject="test subject",
        recipients=["uzezio22@gmail.com"],
        body="test",
        subtype="plain",
    )

    msg = MailMsg(**message.model_dump())
    msg_object = await msg._message("test@example.com")
    assert msg_object._charset is not None
    assert msg_object._charset == "utf-8"
