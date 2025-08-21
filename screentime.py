import psutil
import win32gui
import win32process
import time
import datetime
from datetime import datetime, timedelta
import atexit
import pickle
import os

time_data = {}

file_path = os.path.realpath(__file__)


def get_foreground_exe():   #Get current exe
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return psutil.Process(pid).exe()
    except Exception:
         return None

def save_time_data():
            with open("time_data.pickle", "wb") as f:
                pickle.dump(time_data, f, pickle.HIGHEST_PROTOCOL)
            print("Time data saved at"+file_path)


def mainloop():

    current_exe = get_foreground_exe()  #current_exe = state at the end of the loop
    start_time = time.time()
    tomorrow_date = datetime.today() + timedelta(days=1)
        



    while True:
        time.sleep(1)


        new_exe = get_foreground_exe() 
        if new_exe != current_exe:
            elapsed_time = time.time() - start_time

            if current_exe in time_data: 
                time_data[current_exe] += elapsed_time
            else:
                time_data[current_exe] = elapsed_time

            current_exe = new_exe
            start_time = time.time()


        if datetime.today() >= tomorrow_date:
            save_time_data()    
            time_data.clear()
            tomorrow_date = datetime.today() + timedelta(days=1)



def exit_handler():
    print("Time data saved at"+file_path)
    save_time_data()
atexit.register(exit_handler)

mainloop()
