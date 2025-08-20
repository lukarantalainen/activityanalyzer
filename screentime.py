import psutil
import win32gui
import win32process
import time

time_data = {}


def get_foreground_exe():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return psutil.Process(pid).exe()




def track_window_time():
    current_exe = get_foreground_exe()
    start_time = time.time()

    while True:
        time.sleep(0.5)
        new_exe = get_foreground_exe()
        elapsed_time = time.time() - start_time

        if new_exe != current_exe:
            

            if current_exe in time_data: 
                time_data[current_exe] += elapsed_time
            else:
                time_data[current_exe] = elapsed_time

            print(time_data)

        current_exe = new_exe
        start_time = time.time()

track_window_time()