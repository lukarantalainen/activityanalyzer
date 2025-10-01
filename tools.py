import json
import ctypes
import psutil
import datetime
import os
from config import USER_DATA, TIME_DATA, MOUSE_DATA, KB_DATA, INIT_DATA

def create_files():
    if not os.path.exists(USER_DATA):
        with open(USER_DATA, "w") as f:
            json.dump({"current_date": 0}, f)
    if not os.path.exists(TIME_DATA):
        with open(TIME_DATA, "w") as f:
            json.dump({}, f)
            print("creating")
    if not os.path.exists(MOUSE_DATA):
        with open(MOUSE_DATA, "w") as f:
            json.dump({"buttons": {}, "scroll_ticks": 0, "distance": 0}, f)
    if not os.path.exists(KB_DATA):
        with open(KB_DATA, "w") as f:
            json.dump({}, f)
    if not os.path.exists(INIT_DATA):
        with open(INIT_DATA, "w") as f:
            json.dump(
                {"program_names": {
                "chrome": "Google Chrome",
                "msedge": "Microsoft Edge",
                "firefox": "Mozilla Firefox",
                "code": "Visual Studio Code",
                "notepad++": "Notepad++",
                "spotify": "Spotify",
                "discord": "Discord",
                "slack": "Slack",
                "teams": "Microsoft Teams",
                "word": "Microsoft Word",
                "excel": "Microsoft Excel",
                "powerpnt": "Microsoft PowerPoint",
                "outlook": "Microsoft Outlook",
                "zoom": "Zoom",
                "skype": "Skype",
                "vlc": "VLC Media Player",
                "steam": "Steam",
                "null": "Sleep",
                "taskmgr": "Task Manager",
                "lockapp": "Lockscreen",
                "cs2": "Counter-Strike 2",
                "steamwebhelper": "Steam overlay",
                "explorer": "File Explorer",
                "windowsterminal": "Command Prompt",
                "searchhost": "Windows Search"}}, f)

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)

def clear_json(path):
    with open(path, "w") as f:
        json.dump({}, f)

def save_json(data, path):
    try:
            with open(path, "w") as f:
                json.dump(data, f)
    except Exception as e:
        print(e)

def get_foreground_exe():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return psutil.Process(pid.value).exe()
    except Exception:
         return None

def get_date_str():
    current_date = datetime.date.today()
    date_str = current_date.strftime("%d/%m/%Y")
    return date_str

def check_date():

    user_data = load_json(USER_DATA)
    last_date = user_data["current_date"]
    current_date = get_date_str()

    if current_date != last_date:
        user_data["current_date"] = current_date
        save_json(user_data, USER_DATA)
    else:
        user_data["current_date"] = current_date
