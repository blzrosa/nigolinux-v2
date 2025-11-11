from src.utils.execute import execute_as_root, execute_as_user
from typing import Dict, Union, Literal, List
import shutil
from pathlib import Path
import os
from src.utils.progress import TypedProgressBar

Installer = Union[Literal['pacman'], Literal['yay'], Literal['flatpak']]

def install(to_install: Dict[Installer, List[str]]) -> None:
    for installer, packages in to_install.items():
        if not packages:
            continue
        match installer:
            case 'pacman':
                for package in TypedProgressBar(packages, packages, 'Pacman install'):
                    execute_as_root(['pacman', '-S', '--needed', '--noconfirm', package])
            case 'yay':
                install_yay()
                for package in TypedProgressBar(packages, packages, 'Yay install'):
                    execute_as_user(['yay', '-S', '--needed', '--noconfirm', package])
            case 'flatpak':
                install_flatpak()
                for package in TypedProgressBar(packages, packages, 'Flatpak install'):
                    execute_as_user(['flatpak', 'install', '-y', 'flathub', package])
            case _:
                continue

def install_flatpak() -> None:
    if shutil.which('flatpak'):
        return None
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