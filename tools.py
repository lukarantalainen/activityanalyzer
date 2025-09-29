import json
import os
from config import USER_DATA, TIME_DATA, MOUSE_DATA, KB_DATA, PROGRAM_NAMES

def create_files():
    if not os.path.exists(USER_DATA):
        with open(USER_DATA, "w") as f:
            json.dump({"current_date": 0}, f)
    if not os.path.exists(TIME_DATA):
        with open(TIME_DATA, "w") as f:
            json.dump({}, f)
    if not os.path.exists(MOUSE_DATA):
        with open(MOUSE_DATA, "w") as f:
            json.dump({"buttons": {}, "scroll_ticks": 0, "distance": 0}, f)
    if not os.path.exists(KB_DATA):
        with open(KB_DATA, "w") as f:
            json.dump({}, f)
    if not os.path.exists(PROGRAM_NAMES):
        with open(PROGRAM_NAMES, "w") as f:
            json.dump({"chrome": "Google Chrome", "msedge": "Microsoft Edge", "firefox": "Mozilla Firefox", "code": "Visual Studio Code", "notepad++": "Notepad++", "spotify": "Spotify", "discord": "Discord", "slack": "Slack", "teams": "Microsoft Teams", "word": "Microsoft Word", "excel": "Microsoft Excel", "powerpnt": "Microsoft PowerPoint", "outlook": "Microsoft Outlook", "zoom": "Zoom", "skype": "Skype", "vlc": "VLC Media Player", "steam": "Steam", "null": "Sleep", "taskmgr": "Task Manager", "lockapp": "Lockscreen", "cs2": "Counter-Strike 2", "steamwebhelper": "Steam overlay", "explorer": "File Explorer", "windowsterminal": "Command Prompt", "searchhost": "Windows Search", }, f)

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)
            return {}

def clear_json(path):
    with open(path, "w") as f:
        json.dump({}, f)

def save_json(data, path):
    try:
            with open(path, "w") as f:
                json.dump(data, f)
    except Exception as e:
        print(e)

def reset_all():
    os.remove("time_data.json")
    os.remove("mouse_data.json")
    os.remove("kb_data.json")
    create_files()
