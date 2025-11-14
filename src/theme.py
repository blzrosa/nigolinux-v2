from typing import Dict

from src.utils.execute import execute_as_user
from src.utils.install import install

SETTINGS: Dict[str, str] = {
    "gtk-theme": "catppuccin-mocha-mauve-standard+default",
    "icon-theme": "Papirus-Dark",
    "cursor-theme": "Bibata-Modern-Classic",
    "font-name": "Noto Sans Regular 11",
    "color-scheme": "prefer-dark",
}


def apply_gnome_settings() -> None:
    install(
        {
            "pacman": [
                "qt6-imageformats",
                "dconf",
                "gsettings-desktop-schemas",
                "xdg-desktop-portal-gtk",
            ],
            "yay": [
                "catppuccin-gtk-theme-mocha",
                "papirus-icon-theme",
                "bibata-cursor-theme",
            ],
        }
    )
    for setting, value in SETTINGS.items():
        execute_as_user(["gsettings", "set", "org.gnome.desktop.interface", setting, f'"{value}"'])
