from typing import Dict, List
from pathlib import Path
from src import ASSETS_PATH
import shutil

FONT_CONFIG_DIR: Path = Path("/etc/fonts/conf.d/")
FONT_TEMPLATE = ASSETS_PATH / 'fontconfig.conf'

FONTS_TO_INSTALL: Dict[str, List[str]] = {
    'Pacman': [
        "noto-fonts",
        "ttf-font-awesome",
        "ttf-nerd-fonts-symbols",
        "ttf-jetbrains-mono-nerd",
        "noto-fonts-emoji",
        "noto-fonts-cjk",
        "noto-fonts-extra",
        "ttf-liberation",
        "ttf-dejavu",
        "ttf-roboto",
    ],
    'yay': [
        "jetbrains-mono-nerd-font",
        "adwaita-sans",
    ],
}

def setup_font_config() -> None:
    destination_file: Path = FONT_CONFIG_DIR / FONT_TEMPLATE.name
    shutil.copy(FONT_TEMPLATE, destination_file)