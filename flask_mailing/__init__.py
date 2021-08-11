from .mail import Mail
from .config import  ConnectionConfig
from .schemas import Message, MultipartSubtypeEnum
from . import utils


version_info = (0, 0, 2)

__version__ = ".".join([str(v) for v in version_info])


__author__ = "aniketsarkar@yahoo.com"



__all__ = [
    "Mail", "ConnectionConfig", "Message", "utils", "MultipartSubtypeEnum"
]