import os
from enum import Enum
from typing import List, Union, Any, Optional, Dict
from mimetypes import MimeTypes

from pydantic import BaseModel, EmailStr, validator
from werkzeug.datastructures import FileStorage
from .errors import WrongFile


class MultipartSubtypeEnum(Enum):
    '''
    for more info about Multipart subtypes visit: https://en.wikipedia.org/wiki/MIME#Multipart_subtypes
    '''
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
    recipients: List[EmailStr]
    attachments: List[Any] = []
    subject: str = ""
    body: Optional[Union[str, list]] = None
    template_body: Optional[Union[list, dict]] = None
    html: Optional[Union[str, List, Dict]] = None
    cc: List[EmailStr] = []
    bcc: List[EmailStr] = []
    reply_to: List[EmailStr] = []
    charset: str = "utf-8"
    subtype: Optional[str] = None
    multipart_subtype: MultipartSubtypeEnum = MultipartSubtypeEnum.mixed

    @validator("attachments")
    def validate_file(cls, v):
        temp = []
        mime = MimeTypes()

        for file in v:
            if isinstance(file, str):
                if os.path.isfile(file) and os.access(file, os.R_OK) and validate_path(file):
                    mime_type = mime.guess_type(file)
                    f = open(file, mode="rb")
                    _, file_name = os.path.split(f.name)
                    u = FileStorage(f, file_name, content_type=mime_type[0])
                    temp.append(u)
                else:
                    raise WrongFile(
                        "incorrect file path for attachment or not readable")
            elif isinstance(file, FileStorage):
                temp.append(file)
            else:
                raise WrongFile(
                    "attachments field type incorrect, must be FileStorage or path")
        return temp

    @validator('subtype')
    def validate_subtype(cls, value, values, config, field):
        """Validate subtype field."""
        if values['template_body']:
            return 'html'
        return value


def validate_path(path):
    cur_dir = os.path.abspath(os.curdir)
    requested_path = os.path.abspath(os.path.relpath(path, start=cur_dir))
    common_prefix = os.path.commonprefix([requested_path, cur_dir])
    return common_prefix == cur_dir