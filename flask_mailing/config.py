import os
from pathlib import Path
from typing import Optional

from flask.globals import current_app
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseSettings as Settings
from pydantic import DirectoryPath, EmailStr, conint, validator

from .errors import TemplateFolderDoesNotExist


class ConnectionConfig(Settings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    MAIL_DEBUG: conint(gt=-1, lt=2) = 0
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: Optional[str] = None
    MAIL_TEMPLATE_FOLDER: Optional[DirectoryPath] = None
    SUPPRESS_SEND: conint(gt=-1, lt=2) = 0
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    @validator("MAIL_TEMPLATE_FOLDER")
    def template_folder_validator(cls, v):
        """Validate the template folder directory."""
        if not v:
            return
        if not os.access(str(v), os.R_OK):  # or not path_traversal(v):
            raise TemplateFolderDoesNotExist(
                f"{v!r} is not a valid path to an email template folder"
            )
        return v

    def template_engine(self) -> Environment:
        """Return template environment."""
        folder = self.MAIL_TEMPLATE_FOLDER

        if not folder:
            template_env = current_app.jinja_env

        else:
            template_env: "Environment" = Environment(loader=FileSystemLoader(folder))

        return template_env


def path_traversal(fp: Path) -> bool:
    """Check for path traversal vulnerabilities."""
    base = Path(__file__).parent.parent
    try:
        base.joinpath(fp).resolve().relative_to(base.resolve())
    except ValueError:
        return False
    return True
