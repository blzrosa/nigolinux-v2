from execute import execute_as_root, execute_as_user
from typing import Dict, Union, Literal, List
import shutil
from pathlib import Path
import os

Installer = Union[Literal['pacman'], Literal['yay'], Literal['flatpak']]

def install(to_install: Dict[Installer, List[str]]) -> None:
    for installer, packages in to_install.items():
        if not packages:
            continue
        match installer:
            case 'pacman':
                execute_as_root(['pacman', '-S', '--needed', '--noconfirm'] + packages)
            case 'yay':
                execute_as_user(['yay', '-S', '--needed', '--noconfirm'] + packages)
            case 'flatpak':
                execute_as_user(['flatpak', 'install', '-y', 'flathub'] + packages)
            case _:
                continue

def install_flatpak() -> None:
    install({ 'pacman': ['flatpak'] })

def install_yay() -> None:
    if shutil.which('yay'):
        return None
    temp_dir: Path = Path('/tmp/yay-install')
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    install({ 'pacman': ['git', 'base-devel'] })
    execute_as_user(['git', 'clone', 'https://aur.archlinux.org/yay.git', str(temp_dir)])
    original_dir: Path = Path.cwd()
    os.chdir(temp_dir)
    execute_as_user(['makepkg', '-si', '--noconfirm'])
    os.chdir(original_dir)
    shutil.rmtree(temp_dir)