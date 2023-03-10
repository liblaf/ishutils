import dataclasses
import os
from pathlib import Path

from ..common.run import run
from ..logging import Logger, get_logger
from . import DESKTOP_FILE_INSTALL_DIR


@dataclasses.dataclass(kw_only=True)
class DesktopEntry:
    Type: str = "Application"
    Name: str = ""
    Comment: str = ""
    Path: str = ""
    Exec: str = ""
    Icon: str = ""
    Terminal: bool = False
    Categories: str = ""
    MimeType: str = ""
    GenericName: str = ""
    StartupNotify: str = ""


def make_desktop_file(slug: str, entry: DesktopEntry):
    logger: Logger = get_logger()
    if not entry.Name:
        entry.Name = slug
    filepath = DESKTOP_FILE_INSTALL_DIR / f"{slug}.desktop"
    os.makedirs(Path(filepath).parent, exist_ok=True)
    with open(file=filepath, mode="w") as fp:
        print("[Desktop Entry]", file=fp)
        for key, value in dataclasses.asdict(entry).items():
            if value == "":
                continue
            if isinstance(value, bool):
                value = "true" if value else "false"
            print(f"{key}={value}", file=fp)
    logger.success(f"Desktop Entry: {entry.Name} at {filepath}")
    run(args=["desktop-file-install", "--dir", DESKTOP_FILE_INSTALL_DIR, filepath])
