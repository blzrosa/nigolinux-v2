import os
import shutil
import subprocess
from pathlib import Path

from src import ASSETS_PATH
from src.utils.execute import execute_as_root
from src.utils.install import install
from src.utils.permissions import ensure_root

THEME_NAME = "sddm-nigo-light"
THEMES_DIR: Path = Path("/usr/share/sddm/themes")
THEME_DEST_DIR = THEMES_DIR / THEME_NAME
SDDM_CONFIG_FILE = "/etc/sddm.conf"
SDDM_ASSETS_DIR = ASSETS_PATH / "sddm"
FONTS_DEST_DIR = Path("/usr/share/fonts/")


def apply_sddm_theme():
    ensure_root()

    install(
        {
            "pacman": [
                "sddm",
                "qt6-svg",
                "qt6-virtualkeyboard",
                "qt6-multimedia-ffmpeg",
            ]
        }
    )

    if THEME_DEST_DIR.exists():
        shutil.move(
            THEME_DEST_DIR,
            f"{THEME_DEST_DIR}_{subprocess.check_output(['date', '+%s']).strip().decode()}",
        )
    os.makedirs(THEME_DEST_DIR)
    shutil.copytree(SDDM_ASSETS_DIR, THEME_DEST_DIR, dirs_exist_ok=True)
    fonts_src_dir: Path = THEME_DEST_DIR / "Fonts"
    if fonts_src_dir.is_dir():
        shutil.copytree(fonts_src_dir, FONTS_DEST_DIR, dirs_exist_ok=True)

    sddm_config_content: str = f"[Theme]\nCurrent={THEME_NAME}\n"
    with open(SDDM_CONFIG_FILE, "w") as f:
        f.write(sddm_config_content)
    sddm_conf_d: Path = Path("/etc/sddm.conf.d")
    os.makedirs(sddm_conf_d, exist_ok=True)
    with open(sddm_conf_d / "virtualkbd.conf", "w") as f:
        f.write("[General]\nInputMethod=qtvirtualkeyboard\n")

    execute_as_root(
        ["systemctl", "disable", "display-manager.service"],
        ["systemctl", "enable", "sddm.service", "--force"],
    )
