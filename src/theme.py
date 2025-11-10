from src.utils.execute import execute_as_user
from typing import Dict

SETTINGS: Dict[str, str] = {
    "gtk-theme": "catppuccin-mocha-mauve-standard+default",
    "icon-theme": "Papirus-Dark",
    "cursor-theme": "Bibata-Modern-Classic",
    "font-name": "Noto Sans Regular 11",
    "color-scheme": "prefer-dark",
}

def apply_gnome_settings() -> None:
    for setting, value in SETTINGS.items():
        execute_as_user(["set", "org.gnome.desktop.interface", setting, value])