import os

if os.name == "nt":
    try:
        os.add_dll_directory(r"C:\Windows\System32")
    except (OSError, AttributeError):
        pass

    try:
        os.add_dll_directory(r"C:\Program Files\Git\usr\bin")
    except (OSError, AttributeError):
        pass

from .read import read as read
from .write import write as write
