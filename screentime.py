import ctypes
import psutil
import time
import datetime
from datetime import timedelta
import atexit
import json
import data_analyzer as data
import keyboard
import os
import socket



time_data = {}

with open("time_data.json") as f:
    try:
        time_data = json.load(f)
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

def save_time_data():
    try:
            with open("time_data.json", "w") as f:
                json.dump(time_data, f)
    except IOError:
        print("An IOError has occured.")
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)

def reset_data():
    time_data.clear()

def mainloop():

    with open("user_data.json") as f:
        user_data = json.load(f)
    last_date = user_data.get("current_date")
    current_exe = get_foreground_exe()
    start_time = time.time()

    def get_date_str():
        current_date = datetime.date.today()
        date_str = current_date.strftime("%d/%m/%Y")
        return date_str

    tomorrow_date = datetime.date.today() + timedelta(1)
    tomorrowdatestr = tomorrow_date.strftime("%d/%m/%y")

    update_interval = 60
    save_interval = 300
    last_update = 0 
    last_save = time.time()

    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    user_data = {
        "current_date": get_date_str(),
        "ip_address": ip_address,
    
}
    def save_user_data():
        with open("user_data.json", "w") as f:
            json.dump(user_data, f)

    save_user_data()
    
    keyboard.add_hotkey("ctrl+alt+shift+d", lambda: data.main())
    keyboard.add_hotkey("ctrl+alt+shift+s", lambda: save_time_data())
    keyboard.add_hotkey("ctrl+alt+shift+r", lambda: reset_data())

    while True:
        time.sleep(5)
        new_exe = get_foreground_exe()
        now = time.time()

        if new_exe != current_exe:
            elapsed_time = now - start_time
            if current_exe in time_data: 
                time_data[current_exe] += round(elapsed_time)
            else:
                time_data[current_exe] = round(elapsed_time)
            current_exe = new_exe
            start_time = now
            last_update = now
    
        if now - last_update >= update_interval:
            elapsed_time = now - start_time
            if current_exe in time_data:
                time_data[current_exe] += round(elapsed_time)
            else:
                time_data[current_exe] = round(elapsed_time)
            start_time = now
            last_update = now

        if now - last_save >= save_interval:
            save_time_data()
            last_save = now
        
        if datetime.date.today() >= tomorrow_date or last_date >= tomorrowdatestr:
            elapsed_time = now - start_time
            if current_exe in time_data:
                time_data[current_exe] += round(elapsed_time)
            else:
                time_data[current_exe] + round(elapsed_time)
            
            last_date = get_date_str()
            save_user_data()

            save_time_data()
            time_data.clear()
            start_time = now

            tomorrow_date = datetime.date.today() + timedelta(days=1)

        


print("Next save at", datetime.date.today() + timedelta(days=1))




def exit_handler():
    save_time_data()
    data.main()
    data.exit_countdown()
    return None
atexit.register(exit_handler)

mainloop()