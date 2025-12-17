import subprocess
from typing import List

from src.utils.permissions import check_root, get_sudo_user


def rootify(command: List[str]) -> List[str]:
    if not check_root():
        raise PermissionError("Doesn't have root privileges")
    return ["sudo"] + command if "sudo" not in command else command


def unrootify(command: List[str]) -> List[str]:
    user: str = get_sudo_user()
    return ["sudo", "-u", user] + command


def execute_as_root(*commands: List[str]) -> None:
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)


def execute_as_user(*commands: List[str]) -> None:
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
