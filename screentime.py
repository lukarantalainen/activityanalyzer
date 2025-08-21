import psutil
import win32gui
import win32process
import time
import atexit

time_data = {}


def get_foreground_exe():   #Get current exe
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return psutil.Process(pid).exe()




def track_window_time():
    current_exe = get_foreground_exe()  #current_exe = state at the end of the loop
    start_time = time.time()

    while True:
        time.sleep(0.5)
        new_exe = get_foreground_exe() 

        if new_exe != current_exe:
            elapsed_time = time.time() - start_time

            if current_exe in time_data: 
                time_data[current_exe] += elapsed_time
            else:
                time_data[current_exe] = elapsed_time

            
            current_exe = new_exe
            start_time = time.time()


def exit_handler():
    print(time_data)
        
track_window_time()