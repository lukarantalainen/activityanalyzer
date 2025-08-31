import psutil
import win32gui
import win32process
import time
import datetime
from datetime import timedelta
import atexit
import json
from subprocess import Popen
import data_analyzer as data

time_data = {
    
}


def get_foreground_exe():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return psutil.Process(pid).exe()
    except Exception:
         return None

def save_time_data():
    try:
            with open("time_data.json", "w") as f:
                json.dump(time_data, f)
    except IOError:
        print("An IOError has occured.")


def mainloop():

    current_exe = get_foreground_exe()
    start_time = time.time()
    tomorrow_date = datetime.date.today() + timedelta(1)
    update_interval = 60
    last_update = 0 

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
            save_time_data()
        
        if datetime.date.today() >= tomorrow_date:
            elapsed_time = now - start_time
            if current_exe in time_data:
                time_data[current_exe] += round(elapsed_time)
            else:
                time_data[current_exe] + round(elapsed_time)
            save_time_data()    
            time_data.clear()
            start_time = now
            tomorrow_date = datetime.date.today() + timedelta(days=1)


print("Next save at", datetime.date.today() + timedelta(days=1))




def exit_handler():
    save_time_data()
    data.main()
atexit.register(exit_handler)

mainloop()