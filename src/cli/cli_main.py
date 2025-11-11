import json
import sys
from typing import Callable, Dict, List, Set, Tuple

from src import ASSETS_PATH
from src.cli.cli_utils import clear_console, get_key, handle_quit, print_menu
from src.dotfiles import apply_dotfiles
from src.fonts import apply_fonts
from src.grub import apply_grub_theme
from src.lid import disable_lid_switch
from src.sddm import apply_sddm_theme
from src.theme import apply_gnome_settings
from src.utils.install import Installer, install
from src.utils.permissions import enable_lingering, ensure_root

with open(ASSETS_PATH / "to_install.json", "r") as file:
    TO_INSTALL: Dict[Installer, List[str]] = json.load(file)

TASKS: Dict[str, Tuple[str, Callable[..., None]]] = {
    "1": ("Install Packages", lambda: install(TO_INSTALL)),
    "2": ("Fix shutdown", enable_lingering),
    "3": ("Apply dotfiles", apply_dotfiles),
    "4": ("Apply Fonts", apply_fonts),
    "5": ("Apply GNOME Theme", apply_gnome_settings),
    "6": ("Apply SDDM Theme", apply_sddm_theme),
    "7": ("Apply GRUB Theme", apply_grub_theme),
    "8": ("Disable Lid Suspend", disable_lid_switch),
}

MASTER_TASK_ORDER: List[str] = [str(i) for i in range(1, 8)]
MENU_OPTIONS = [
    ("Run all main tasks (1-7)", "0"),
    ("Install Packages", "1"),
    ("Fix shutdown", "2"),
    ("Apply dotfiles", "3"),
    ("Apply Fonts", "4"),
    ("Apply GNOME Theme", "5"),
    ("Apply SDDM Theme", "6"),
    ("Apply GRUB Theme", "7"),
    ("Disable Lid Suspend", "8"),
    ("Quit", "q"),
]


def run_tasks(task_id_set: Set[str]) -> None:
    tasks_to_run_map: Dict[str, Tuple[str, Callable[..., None]]] = {}
    final_task_ids: Set[str] = set(task_id_set)
    if "0" in final_task_ids:
        final_task_ids.union(set(MASTER_TASK_ORDER))
    for task_id in MASTER_TASK_ORDER:
        if task_id in final_task_ids:
            tasks_to_run_map[task_id] = TASKS[task_id]
    if str(len(MASTER_TASK_ORDER)) in final_task_ids:
        tasks_to_run_map[str(len(MASTER_TASK_ORDER))] = TASKS[
            str(len(MASTER_TASK_ORDER))
        ]
    tasks_to_run = list(tasks_to_run_map.values())
    total_tasks: int = len(tasks_to_run)
    if total_tasks == 0:
        print("No valid tasks selected to run.")
        return
    print(f"\nStarting {total_tasks} selected task(s)...")
    for _, (description, task_function) in enumerate(tasks_to_run):
        try:
            task_function()
        except Exception as e:
            print(f"[FAILED] {description}")
            print(f"Task '{description}' failed with an error:\n{e}")
            if len(tasks_to_run) > 1:
                while True:
                    choice = (
                        input(
                            "Do you want to continue with the next tasks? (y/n): "
                        )
                        .lower()
                        .strip()
                    )
                    if choice == "n":
                        print(
                            "Aborting remaining tasks. Returning to main menu."
                        )
                        return
                    elif choice == "y":
                        print("Continuing with next task...")
                        break
            else:
                input("Press Enter to return to the menu.")
                return
    print("\n\nAll selected tasks completed successfully.")
    input("Press Enter to return to the menu.")


def main() -> None:
    try:
        ensure_root()
    except PermissionError as e:
        print(
            f"Error: {e}\nPlease run this script as root or with sudo.",
            file=sys.stderr,
        )
        sys.exit(1)

    current_idx: int = 0
    selected_options: Set[int] = set()
    num_menu_items: int = len(MENU_OPTIONS)
    total_selectable_lines: int = num_menu_items + 1

    while True:
        print_menu(current_idx, selected_options, MENU_OPTIONS)
        key = get_key()
        if key is None:
            continue
        match key:
            case "UP":
                current_idx = (current_idx - 1) % total_selectable_lines
            case "DOWN":
                current_idx = (current_idx + 1) % total_selectable_lines
            case "SPACE":
                if current_idx >= num_menu_items:  # Can't select <OK>
                    continue
                if current_idx in selected_options:
                    selected_options.remove(current_idx)
                else:
                    selected_options.add(current_idx)
            case "ENTER":
                if current_idx == num_menu_items:
                    if not selected_options:
                        continue
                    task_ids_to_run: Set[str] = set()
                    for idx in selected_options:
                        _, task_value = MENU_OPTIONS[idx]
                        if task_value == "q":
                            handle_quit()
                        task_ids_to_run.add(task_value)
                    clear_console()
                    run_tasks(task_ids_to_run)
                    selected_options.clear()

                elif current_idx < num_menu_items:
                    _, task_value = MENU_OPTIONS[current_idx]

                    if task_value == "q":
                        handle_quit()

                    clear_console()
                    run_tasks({task_value})

                    selected_options.discard(current_idx)
            case "q":
                handle_quit()
            case "CTRL_C":
                handle_quit()
