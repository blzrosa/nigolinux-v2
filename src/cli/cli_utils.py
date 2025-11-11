import os
import sys
from typing import Optional, Tuple, Set, List, Literal, Union
import tty
import termios

def clear_console() -> None:
    os.system('clear')

ValidKey = Optional[Union[Literal['UP'], Literal['DOWN'], Literal['ENTER'], Literal['SPACE'], Literal['CTRL_C'], Literal['q']]]

def get_key() -> ValidKey:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        
        if ch == '\x1b':
            seq = sys.stdin.read(2)
            if seq == '[A':
                return 'UP'
            elif seq == '[B':
                return 'DOWN'
        elif ch == '\r' or ch == '\n':
            return 'ENTER'
        elif ch == ' ':
            return 'SPACE'
        elif ch == '\x03':
            return 'CTRL_C'
        elif ch == 'q' or ch == 'Q':
            return 'q'
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def print_menu(current_idx: int, selected_options: Set[int], menu_options: List[Tuple[str, str]]) -> None:
    clear_console()
    print("╔════════════════════════════════╗")
    print("║     NigoLinux-v2 Installer     ║")
    print("╚════════════════════════════════╝")
    print("┌────────────────────────────────┐")
    print("│        Select  options         │")
    print("│                                │")
    for i, (label, _) in enumerate(menu_options):
        cursor: str = ">" if i == current_idx else " "
        selected: str = "x" if i in selected_options else " "
        print(f"│ {cursor} [{selected}] {label:<24} │")
    if current_idx == len(menu_options):
        print("│                         [OK]   │")
    else:
        print("│                         <OK>   │")
    print("└────────────────────────────────┘")
    print("\nUse Arrow Keys (Up/Down) to navigate.")
    print("Press [Spacebar] to toggle selection.")
    print("Press [Enter] to run (on <OK> or single item).")
    print("Press [q] or [Ctrl+C] to quit.")

def handle_quit() -> None:
    clear_console()
    print("See you again at 25:00.")
    sys.exit(0)