import io
import os
import sys
from enum import Enum
from mimetypes import MimeTypes
from typing import Dict, List, Optional, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import BaseModel, EmailStr, validator
from werkzeug.datastructures import FileStorage

from .errors import WrongFile


class MultipartSubtypeEnum(Enum):
    """
    for more info about Multipart subtypes visit: https://en.wikipedia.org/wiki/MIME#Multipart_subtypes
    """

    mixed = "mixed"
    digest = "digest"
    alternative = "alternative"
    related = "related"
    report = "report"
    signed = "signed"
    encrypted = "encrypted"
    form_data = "form-data"
    mixed_replace = "x-mixed-replace"
    byterange = "byterange"


class Message(BaseModel):
    recipients: List["EmailStr"]
    attachments: List[Union[FileStorage, Dict, str]] = []
    subject: str = ""
    body: Optional[Union[str, list]] = None
    template_body: Optional[Union[list, dict]] = None
    template_params: Optional[Union[list, dict]] = None
    html: Optional[Union[str, List, Dict]] = None
    cc: List["EmailStr"] = []
    bcc: List["EmailStr"] = []
    reply_to: List["EmailStr"] = []
    charset: str = "utf-8"
    subtype: Optional[str] = None
    multipart_subtype: MultipartSubtypeEnum = MultipartSubtypeEnum.mixed

    @validator("template_params")
    def validate_template_params(cls, value, values):

        if values.get("template_body", None) is None:
            values["template_body"] = value
        return value

    @validator("attachments")
    def validate_file(cls, v):
        temp = []
        mime = MimeTypes()

        for file in v:
            file_meta = None
            if isinstance(file, dict):
                keys = file.keys()
                if "file" not in keys:
                    raise WrongFile('missing "file" key')
                file_meta = dict.copy(file)
                del file_meta["file"]
                file = file["file"]
            if isinstance(file, str):
                if (
                    os.path.isfile(file)
                    and os.access(file, os.R_OK)
                    and validate_path(file)
                ):
                    mime_type = mime.guess_type(file)
                    f = open(file, mode="rb")
                    _, file_name = os.path.split(f.name)
                    u = FileStorage(f, file_name, content_type=mime_type[0])
                    temp.append((u, file_meta))
                else:
                    raise WrongFile(
                        "incorrect file path for attachment or not readable"
                    )
            elif isinstance(file, FileStorage):
                temp.append((file, file_meta))
            else:
                raise WrongFile(
                    "attachments field type incorrect, must be FileStorage or path"
                )
        return temp

    def add_recipient(self, recipient: str) -> Literal[True]:
        """
        Adds another recipient to the message.

        :param recipient: email address of recipient.
        """
        self.recipients.append(recipient)
        return True

    def attach(
        self,
        filename: str,
        data: Union[bytes, str],
        content_type: dict = None,
        disposition: str = "attachment",
        headers: dict = {},
    ) -> Literal[True]:
        """
        Adds an attachment to the message.

        :param `filename`: filename of attachment
        :param `data`: the raw file data
        :param `content_type`: file mimetype
        :param `disposition`: content-disposition (if any)
        :param `headers`: dictionary of headers
        """
        if content_type is None:
            mime = MimeTypes()
            content_type = mime.guess_type(filename)

        fsob: "FileStorage" = FileStorage(
            io.BytesIO(data), filename, content_type=content_type, headers=headers
        )
        fsob.disposition = disposition
        self.attachments.append(fsob)
        return True

    @validator("subtype")
    def validate_subtype(cls, value, values, config, field):
        """Validate subtype field."""
        if values.get("template_body"):
            return "html"
        return value

    class Config:
        arbitrary_types_allowed = True


def validate_path(path):
    cur_dir = os.path.abspath(os.curdir)
    requested_path = os.path.abspath(os.path.relpath(path, start=cur_dir))
    common_prefix = os.path.commonprefix([requested_path, cur_dir])
    return common_prefix == cur_dir
