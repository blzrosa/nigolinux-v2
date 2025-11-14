from pathlib import Path
import os

BASE_PATH: Path = Path(__file__).resolve().parent.parent
SRC_PATH: Path = BASE_PATH / "src"
ASSETS_PATH: Path = BASE_PATH / "assets"
HOME_PATH: Path = Path(os.path.expanduser(f'~{os.getenv('SUDO_USER') or os.getenv('USERNAME')}'))

if __name__ == "__main__":
    print("BASE_PATH:", BASE_PATH)
    print("SRC_PATH:", SRC_PATH)
    print("ASSETS_PATH:", ASSETS_PATH)
    print("HOME_PATH:", HOME_PATH)
