# src/paths.py
import sys
from pathlib import Path


def get_base_path() -> Path:
    """Repo root when run from source; the folder containing the .exe when frozen.

    Deliberately NOT sys._MEIPASS: that's a temp extraction dir PyInstaller
    unpacks bundled data into, not a stable place for user-supplied files
    like ROMs sitting next to the .exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
