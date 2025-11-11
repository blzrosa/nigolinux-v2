from pathlib import Path

BASE_PATH: Path = Path(__file__).resolve().parent.parent
SRC_PATH: Path = BASE_PATH / 'src'
ASSETS_PATH: Path = BASE_PATH / 'assets'
HOME_PATH: Path = Path('~').expanduser()

if __name__ == '__main__':
    print('BASE_PATH:', BASE_PATH)
    print('SRC_PATH:', SRC_PATH)
    print('ASSETS_PATH:', ASSETS_PATH)
    print('HOME_PATH:', HOME_PATH)