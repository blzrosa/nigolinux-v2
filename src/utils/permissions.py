import os
import subprocess
from enum import Enum
from glob import glob
from typing import Optional, Tuple

from src.utils.progress import TypedProgressBar


class FilePermissions(Enum):
    read = "r"
    write = "w"
    execute = "x"


class SudoError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_user() -> str:
    return os.getlogin()


def get_sudo_user() -> str:
    sudo_user: Optional[str] = os.getenv("SUDO_USER")
    if sudo_user is None:
        raise SudoError("Sudo user not found")
    return sudo_user


def check_root() -> bool:
    return os.geteuid() == 0


def ensure_root() -> None:
    if not check_root():
        raise PermissionError


def enable_lingering() -> None:
    try:
        subprocess.run(
            ["loginctl", "enable-linger", get_sudo_user()],
            check=True,
            capture_output=True,
            text=True,
        )
        return None
    except subprocess.CalledProcessError as e:
        if "already exists" in e.stderr:
            return None
        raise e


def add_permissions(
    patterns: list[str],
    permissions: Tuple[FilePermissions, ...] = (FilePermissions.execute,),
) -> None:
    for pattern in TypedProgressBar(
        patterns, labels=patterns, title="Adding Permissions"
    ):
        scripts = glob(pattern)
        if not scripts:
            continue
        command: list[str] = [
            "chmod",
            f"+{''.join([permission.value for permission in permissions])}",
        ] + scripts
        subprocess.run(command, check=True, capture_output=True, text=True)
