import os
import pwd
import shutil
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from src import ASSETS_PATH, HOME_PATH
from src.utils.execute import execute_as_root
from src.utils.permissions import FilePermissions, add_permissions, get_sudo_user
from src.utils.progress import ProgressBar


SOURCE_CONFIG: Path = ASSETS_PATH / ".config"
dest_config: Path = HOME_PATH / ".config"
backup_config: Path = HOME_PATH / ".config.old"
BRUTE_IMAGES_DIR = ASSETS_PATH / "wallpapers-compressed"
PROCESSED_IMAGES_DIR = dest_config / "wallpapers"

def decompress_single_image(image_name: str) -> str:
    input_path = BRUTE_IMAGES_DIR / image_name
    base_name = Path(image_name).stem  # Filename without extension
    output_path = PROCESSED_IMAGES_DIR / f'{base_name}.webp'
    
    # Run the conversion as root
    execute_as_root([
        "magick", str(input_path),
        "-format", "webp", "-alpha", "off", "-define", "webp:lossless=true",
        str(output_path)
    ])
    os.chmod(str(output_path), 0o666)
    
    return str(output_path)

def decompress_images() -> None:
    os.makedirs(PROCESSED_IMAGES_DIR, exist_ok=True)
    processed_bases = {Path(f).stem for f in os.listdir(PROCESSED_IMAGES_DIR)}
    brute_images = os.listdir(BRUTE_IMAGES_DIR)
    to_process = [img for img in brute_images if Path(img).stem not in processed_bases]
    if not to_process:
        print("No new images to process. All done!")
        return
    print(f"Processing {len(to_process)} images in parallel...")
    max_workers = min(8, len(to_process), os.cpu_count() or 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_image = {
            executor.submit(decompress_single_image, image): image
            for image in to_process
        }
        for _ in ProgressBar(as_completed(future_to_image), title='Decompressing Image'):
            pass

def apply_dotfiles() -> None:
    if not SOURCE_CONFIG.is_dir():
        raise FileNotFoundError
    if dest_config.exists() and backup_config.exists():
        shutil.rmtree(backup_config)
    shutil.move(dest_config, backup_config)
    shutil.copytree(SOURCE_CONFIG, dest_config)
    decompress_images()
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
