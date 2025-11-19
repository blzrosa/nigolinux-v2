from typing import Dict
from src.utils.execute import execute_as_user
from src.utils.install import install

SETTINGS: Dict[str, str] = {
    "gtk-theme": "Adwaita-dark",
    "icon-theme": "Papirus-Dark",
    "cursor-theme": "PJSK N25 Animated",
    "font-name": "Noto Sans Regular 11",
    "color-scheme": "prefer-dark",
}

def setup_cursor() -> None:
    execute_as_user(["bash", "-c", "mkdir -p ~/.icons/default/"])
    index_content = "[Icon Theme]\\nInherits = 'PJSK N25 Animated'"
    execute_as_user(["bash", "-c", f"echo -e \"{index_content}\" > ~/.icons/default/index.theme"])
    target = "/usr/share/icons/PJSK N25 Animated/cursors"
    link_name = "~/.icons/default/cursors"
    execute_as_user(["bash", "-c", f"rm -rf \"{link_name}\" && ln -s \"{target}\" \"{link_name}\""])


def apply_gnome_settings() -> None:
    install(
        {
            "pacman": [
                "qt6-imageformats",
                "dconf",
                "gsettings-desktop-schemas",
                "xdg-desktop-portal-gtk",
                "python-pywal", 
                "papirus-icon-theme",
                "python-setuptools",
            ],
            "yay": [
                "pjsk-cursor-theme",
                "pywalfox",
                "python-haishoku",
            ],
        }
    )

    for setting, value in SETTINGS.items():
        execute_as_user(["gsettings", "set", "org.gnome.desktop.interface", setting, f'"{value}"'])
    
    setup_cursor()