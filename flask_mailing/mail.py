import typing as t
from contextlib import contextmanager

import blinker
from pydantic import BaseModel, EmailStr

from .config import ConnectionConfig
from .connection import Connection
from .errors import PydanticClassRequired
from .msg import MailMsg
from .schemas import Message

if t.TYPE_CHECKING:
    from flask import Flask

version_info = (0, 2, 0)


class _MailMixin:

    name = "Flask Mailing"
    version = ".".join([str(v) for v in version_info])

    @contextmanager
    def record_messages(self):
        """Records all messages. Use in unit tests for example::
            with mail.record_messages() as outbox:
                response = app.test_client.get("/email-sending-view/")
                assert len(outbox) == 1
                assert outbox[0].subject == "testing"
        You must have blinker installed in order to use this feature.
        :versionadded: 0.4
        """

        if not email_dispatched:
            raise RuntimeError("blinker must be installed")

        outbox = []

        def _record(message):
            outbox.append(message)

        email_dispatched.connect(_record)

        try:
            yield outbox
        finally:
            email_dispatched.disconnect(_record)


class Mail(_MailMixin):
    """
    Flask mail system sending mails(individual, bulk)
    attachments(individual, bulk).

    :param app: Optional param, the Flask application.

    """

    def __init__(self, app: t.Optional["Flask"] = None) -> None:

        if app is not None:
            self.init_app(app)

    def init_app(self, app: "Flask") -> None:

        self.config = ConnectionConfig(
            MAIL_USERNAME=app.config.get("MAIL_USERNAME"),
            MAIL_PASSWORD=app.config.get("MAIL_PASSWORD"),
            MAIL_PORT=app.config.get("MAIL_PORT", 465),
            MAIL_SERVER=app.config.get("MAIL_SERVER"),
            MAIL_USE_TLS=app.config.get("MAIL_USE_TLS", False),
            MAIL_USE_SSL=app.config.get("MAIL_USE_SSL", True),
            MAIL_DEBUG=app.config.get("MAIL_DEBUG", 0),
            MAIL_FROM_NAME=app.config.get("MAIL_FROM_NAME", None),
            MAIL_TEMPLATE_FOLDER=app.config.get("MAIL_TEMPLATE_FOLDER", None),
            SUPPRESS_SEND=app.config.get("SUPPRESS_SEND", 0),
            USE_CREDENTIALS=app.config.get("USE_CREDENTIALS", True),
            VALIDATE_CERTS=app.config.get("VALIDATE_CERTS", True),
            MAIL_FROM=app.config.get(
                "MAIL_FROM",
                app.config.get("MAIL_DEFAULT_SENDER", app.config.get("MAIL_USERNAME")),
            ),
        )
        app.extensions["mailing"] = self

    async def get_mail_template(self, env_path, template_name):
        return env_path.get_template(template_name)

    @staticmethod
    def make_dict(data):
        try:
            return dict(data)
        except ValueError:
            raise ValueError(
                f"Unable to build template data dictionary - {type(data)} is an invalid source data type"
            )

    async def __prepare_message(self, message: Message, template=None):
        if template is not None:
            template_body = message.template_body
            if template_body and not message.html:
                if isinstance(template_body, list):
                    message.template_body = template.render({"body": template_body})
                else:
                    template_data = self.make_dict(template_body)
                    message.template_body = template.render(**template_data)

                message.subtype = "html"
            elif message.html:
                if isinstance(template_body, list):
                    message.template_body = template.render({"body": template_body})
                else:
                    template_data = self.make_dict(template_body)
                    message.template_body = template.render(**template_data)
        msg = MailMsg(**message.dict())
        if self.config.MAIL_FROM_NAME is not None:
            sender = f"{self.config.MAIL_FROM_NAME} <{self.config.MAIL_FROM}>"
        else:
            sender = self.config.MAIL_FROM
        return await msg._message(sender)

    async def send_message(self, message: Message, template_name=None):
        """
        to send the message object.

        :param `message`: The object of the Message pydantic class.
        :param `template_name`: if you are about to render any template 
        with the mail please provide the name of the template by using this param.

        ### For example => 
        ```python
        @app.get("/email")
        async def simple_send():
            message = Message(
                subject="Flask-Mailing module",
                recipients=["aniketsarkar@yahoo.com"],
                body="This is the basic email body",
                )
            await mail.send_message(message)
            return jsonify(status_code=200, content={"message": "email has been sent"})
        ```
        """
        if not issubclass(message.__class__, BaseModel):
            raise PydanticClassRequired(
                """Message schema should be provided from Message class, check example below:
         \nfrom flask_mailing import Message  \nmessage = Message(\nsubject = "subject",\nrecipients = ["list_of_recipients"],\nbody = "Hello World",\ncc = ["list_of_recipients"],\nbcc = ["list_of_recipients"],\nreply_to = ["list_of_recipients"],\nsubtype = "plain")
         """
            )

        if template_name:
            template = await self.get_mail_template(
                self.config.template_engine(), template_name
            )
            msg = await self.__prepare_message(message, template)
        else:
            msg = await self.__prepare_message(message)

        async with Connection(self.config) as session:
            if not self.config.SUPPRESS_SEND:
                await session.session.send_message(msg)

            email_dispatched.send(msg)

    async def send_mail(
        self,
        subject:str,
        message:str,
        recipients:t.List[EmailStr],
        html_message:t.Optional[str]=None,
        **msgkwargs
        ) -> None:
        """
        send a simple email by using this simple `send_mail` method.

        :param `subject`: A String containing the subject of the message.
        :param `message`: A string containing the message body.
        :param `recipients`: A list of strings, each an email address. 
        Each member of recipients will see the other recipients 
        in the “To:” field of the email message
        :param `msgkwargs` : the kwargs based parameters for `Message` class.

        ### For example => 
        ```python
        @app.get('/send-mail')
        async def send_mail():
            await mail.send_mail('subject', "message-new", [recipient@email.com])
            return {'msg' : 'success'}
        ```
        """
        message = Message(
            subject=subject,
            recipients=recipients,
            body=message,
            html=html_message,
            **msgkwargs
        )
        await self.send_message(message)

    async def send_mass_mail(
        self,
        datatuple:t.Tuple[t.Tuple[str, str, t.List[EmailStr]]]
        ):
        """
        To handle mass mailing.

        :param `datatuple`: is a tuple in which each element is in this format:
        ```bash
        (subject, message, recipients)
        ```
        """
        for data in datatuple:
            await self.send_mail(*data)


signals = blinker.Namespace()

email_dispatched = signals.signal(
    "email-dispatched",
    doc="""
    Signal sent when an email is dispatched. This signal will also be sent
    in testing mode, even though the email will not actually be sent.
    """,
)