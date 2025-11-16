import os
import pwd
import shutil
from pathlib import Path
from typing import List

from src import ASSETS_PATH, HOME_PATH
from src.utils.permissions import FilePermissions, add_permissions, get_sudo_user

SOURCE_CONFIG: Path = ASSETS_PATH / ".config"


def apply_dotfiles() -> None:
    dest_config: Path = HOME_PATH / ".config"
    backup_config: Path = HOME_PATH / ".config.old"

    if not SOURCE_CONFIG.is_dir():
        raise FileNotFoundError
    if dest_config.exists() and backup_config.exists():
        shutil.rmtree(backup_config)
    shutil.move(dest_config, backup_config)
    shutil.copytree(SOURCE_CONFIG, dest_config)
    user_info = pwd.getpwnam(get_sudo_user())
    uid, gid = user_info.pw_uid, user_info.pw_gid
    os.chown(dest_config, uid, gid)
    for root, dirs, files in os.walk(dest_config):
        for d in dirs:
            os.chown(os.path.join(root, d), uid, gid)
        for f in files:
            os.chown(os.path.join(root, f), uid, gid)
    script_dirs_patterns: List[str] = [
        str(HOME_PATH / ".config/hypr/scripts/*.sh"),
        str(HOME_PATH / ".config/waybar/scripts/*.sh"),
    ]
    add_permissions(script_dirs_patterns, (FilePermissions.execute,))
    return None
