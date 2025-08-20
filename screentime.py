import psutil
import win32gui
import win32process
import time

time_data = dict()

for cycle in range(5):
    window_id = win32gui.GetForegroundWindow()

    _, pid = win32process.GetWindowThreadProcessId(window_id)

    path = psutil.Process(pid).exe()

    print(path)

    start_time = 0

    window_title = ""
    new_window_title = win32gui.GetForegroundWindow()

    start_time = time.time()




    def in_list_check():
        if str(path) in time_data:
            time_data[str(path)] += start_time
            print(time_data)
        else:
            time_data[str(path)] = start_time
            print(time_data)

    in_list_check()
    time.sleep(1)