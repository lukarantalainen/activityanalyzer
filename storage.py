import json

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)
            return {}

time_data = load_json("time_data.json")
mouse_data = load_json("mouse_data.json")
kb_data = list(load_json("kb_data.json"))
key_counter = {}
program_names = {"chrome": "Google Chrome", "msedge": "Microsoft Edge", "firefox": "Mozilla Firefox", "code": "Visual Studio Code", "notepad++": "Notepad++", "spotify": "Spotify", "discord": "Discord", "slack": "Slack", "teams": "Microsoft Teams", "word": "Microsoft Word", "excel": "Microsoft Excel", "powerpnt": "Microsoft PowerPoint", "outlook": "Microsoft Outlook", "zoom": "Zoom", "skype": "Skype", "vlc": "VLC Media Player", "steam": "Steam", "null": "Sleep", "taskmgr": "Task Manager", "lockapp": "Lockscreen", "cs2": "Counter-Strike 2", "steamwebhelper": "Steam overlay", "explorer": "File Explorer"}
