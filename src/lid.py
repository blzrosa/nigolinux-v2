import os
from src.utils.permissions import ensure_root
from typing import List

LOGIND_CONF_PATH = '/etc/systemd/logind.conf'

def disable_lid_switch():
    ensure_root()

    if os.path.exists(LOGIND_CONF_PATH):
        with open(LOGIND_CONF_PATH, 'r') as f:
            lines = f.readlines()
    else:
        lines: List[str] = []
    new_lines: List[str] = []
    found: List[bool] = [False, False, False]
    login_section_index: int = -1

    for i, line in enumerate(lines):
        stripped_line: str = line.strip()
        
        if stripped_line == '[Login]':
            login_section_index = i
        
        if stripped_line.startswith('HandleLidSwitch=') or stripped_line.startswith('#HandleLidSwitch='):
            new_lines.append('HandleLidSwitch=ignore\n')
            found[0] = True
        
        elif stripped_line.startswith('HandleLidSwitchExternalPower=') or stripped_line.startswith('#HandleLidSwitchExternalPower='):
            new_lines.append('HandleLidSwitchExternalPower=ignore\n')
            found[1] = True
        
        elif stripped_line.startswith('HandleLidSwitchDocked=') or stripped_line.startswith('#HandleLidSwitchDocked='):
            new_lines.append('HandleLidSwitchDocked=ignore\n')
            found[2] = True
        
        else:
            new_lines.append(line)
    
    if login_section_index == -1:
        new_lines.append('\n[Login]\n')
        new_lines.append('HandleLidSwitch=suspend\nHandleLidSwitchExternalPower=suspend\nHandleLidSwitchDocked=ignore\n')
    else:
        if not found[0]:
            new_lines.insert(login_section_index + 1, 'HandleLidSwitch=ignore\n')
        if not found[1]:
            new_lines.insert(login_section_index + 1, 'HandleLidSwitchExternalPower=ignore\n')
        if not found[2]:
            new_lines.insert(login_section_index + 1, 'HandleLidSwitchDocked=ignore\n')
        
    with open(LOGIND_CONF_PATH, 'w') as f:
        f.writelines(new_lines)