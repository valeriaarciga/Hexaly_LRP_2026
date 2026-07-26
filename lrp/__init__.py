import os

if os.name == "nt":
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if path and os.path.exists(path):
            try:
                os.add_dll_directory(path)
            except (OSError, AttributeError, ValueError):
                pass

from .read import read as read
from .write import write as write
