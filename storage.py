import utils
import json
import os 

def create_files():
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("user_data.json"):
        with open("user_data.json", "w") as f:
            json.dump({"current_date": 0}, f)
    if not os.path.exists("kb_data.json"):
        with open("kb_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("mouse_data.json"):
        with open("mouse_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("program_names.json"):
        with open("prorgram_names.json", "w") as f:
            json.dump({"chrome": "Google Chrome", "msedge": "Microsoft Edge", "firefox": "Mozilla Firefox", "code": "Visual Studio Code", "notepad++": "Notepad++", "spotify": "Spotify", "discord": "Discord", "slack": "Slack", "teams": "Microsoft Teams", "word": "Microsoft Word", "excel": "Microsoft Excel", "powerpnt": "Microsoft PowerPoint", "outlook": "Microsoft Outlook", "zoom": "Zoom", "skype": "Skype", "vlc": "VLC Media Player", "steam": "Steam", "null": "Sleep", "taskmgr": "Task Manager", "lockapp": "Lockscreen", "cs2": "Counter-Strike 2", "steamwebhelper": "Steam overlay", "explorer": "File Explorer", "windowsterminal": "Command prompt", "searchhost": "Windows Search"}, f)

create_files()

time_data = utils.load_json("time_data.json")
mouse_data = utils.load_json("mouse_data.json")
kb_data = list(utils.load_json("kb_data.json"))
key_counter = {}
program_names = {"chrome": "Google Chrome", "msedge": "Microsoft Edge", "firefox": "Mozilla Firefox", "code": "Visual Studio Code", "notepad++": "Notepad++", "spotify": "Spotify", "discord": "Discord", "slack": "Slack", "teams": "Microsoft Teams", "word": "Microsoft Word", "excel": "Microsoft Excel", "powerpnt": "Microsoft PowerPoint", "outlook": "Microsoft Outlook", "zoom": "Zoom", "skype": "Skype", "vlc": "VLC Media Player", "steam": "Steam", "null": "Sleep", "taskmgr": "Task Manager", "lockapp": "Lockscreen", "cs2": "Counter-Strike 2", "steamwebhelper": "Steam overlay", "explorer": "File Explorer"}
