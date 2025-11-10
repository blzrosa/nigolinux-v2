import os
from typing import Optional, Tuple
import subprocess
from glob import glob
from enum import Enum
import sys

from progress import TypedProgressBar

class FilePermissions(Enum):
    read = 'r'
    write = 'w'
    execute = 'x'

class SudoError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def get_user() -> str:
    return os.getlogin()

def get_sudo_user() -> str:
    sudo_user: Optional[str] = os.getenv("SUDO_USER")
    if sudo_user is None:
        raise SudoError('Sudo user not found')
    return sudo_user

def check_root() -> bool:
    return os.geteuid == 0

def ensure_root() -> None:
    if not check_root():
        sys.exit(1)

def enable_lingering(user: str) -> bool:
    try:
        subprocess.run(
            ["loginctl", "enable-linger", user],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        if "already exists" in e.stderr:
            return False
        raise e

def add_permissions(
        patterns: list[str], 
        permissions: Tuple[FilePermissions, ...] = (FilePermissions.execute,)
        ) -> None:
    for pattern in TypedProgressBar(patterns, labels=patterns, title='Adding Permissions'):
        scripts = glob(pattern)
        if not scripts:
            continue
        command: list[str] = ['chmod', f'+{''.join([permission.value for permission in permissions])}'] + scripts
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )