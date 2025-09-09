import ctypes
import psutil
import time
import datetime
from datetime import timedelta
import atexit
import json
import data_analyzer as data
import matplotlib.pyplot as plt
from PIL import Image
import keyboard
import os
import socket
import mouse

time_data = {}

if not os.path.exists("time_data.json"):
    with open("time_data.json", "w") as f:
        json.dump({}, f)

with open("time_data.json") as f:
    try:
        time_data = json.load(f)
    except Exception as e:
        print(e)

with open("program_names.json") as apps:
    program_names = json.load(apps)

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
            print("Time data succesfully saved!")
    except IOError:
        print("An IOError has occured.")

def display_data():
    save_time_data()
    final_data = {}
    for key, value in time_data.items():
        app = os.path.basename(key).lower()
        app =  os.path.splitext(app)[0].lower()
        if app in program_names:
            app = program_names[app]
            final_data[app] = final_data.get(app, 0) + round(value/60, 2)
        else:
            final_data[app.title()] = final_data.get(app, 0) + round(value/60, 2)

    keys = list(final_data.keys())
    values = list(final_data.values())

    fig, ax = plt.subplots()
    plt.bar(keys, values)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
    fig.subplots_adjust(left=0.15, bottom=0.18, right=0.97)
    plt.xlabel('Applications')
    plt.ylabel('Time Spent (Minutes)')
    plt.title('Screen Time Data')
    plt.savefig("data.png")
    plt.draw()
    plt.show()
    plt.pause(0.01)

def mainloop():

    
    
   
    gather_data() 

        
def gather_data():
    current_exe = get_foreground_exe()
    start_time = time.time()

    

    with open("user_data.json", "r") as f:
        user_data = json.load(f)

    def get_date_str():
        current_date = datetime.date.today()
        date_str = current_date.strftime("%d/%m/%Y")
        return date_str
    
    def get_tomorrow_date():
        tomorrow_date = datetime.date.today() + timedelta(1)
        tomorrowdatestr = tomorrow_date.strftime("%d/%m/%y")
        return tomorrowdatestr

    def save_user_data():
        with open("user_data.json", "w") as f:
            json.dump(user_data, f)


    def check_date():
        last_date = user_data.get("current_date")
        if get_date_str() > last_date:

            save_user_data()
            time_data.clear()

            with open("time_data.json", "w") as f:
                json.dump({}, f)

    check_date()
    

    update_interval = 60
    save_interval = 300
    last_update = 0
    last_save = time.time()

    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    user_data = {
        "current_date": get_date_str(),
}
    save_user_data()
    
    keyboard.add_hotkey("ctrl+alt+shift+d", lambda: save_time_data())

    while True:
        time.sleep(5)
        new_exe = get_foreground_exe()
        now = time.time()
        check_date()
        save_time_data()
        display_data()

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







            

print("Next save at", datetime.date.today() + timedelta(days=1))




def exit_handler():
    save_time_data()
    data.main()
    data.exit_countdown()
    return None
atexit.register(exit_handler)

mainloop()