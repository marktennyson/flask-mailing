from . import utils
from .config import ConnectionConfig
from .mail import Mail
from .schemas import Message as Message
from .schemas import MultipartSubtypeEnum as MultipartSubtypeEnum

version_info = (0, 1, 0)

__version__ = ".".join([str(v) for v in version_info])


__author__ = "aniketsarkar@yahoo.com"


__all__ = ["Mail", "ConnectionConfig", "Message", "utils", "MultipartSubtypeEnum"]
