import ctypes
import psutil
import time
import datetime
from datetime import timedelta
import atexit
import json
from matplotlib.figure import Figure
import tkinter
from tkinter import *
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import Image
import keyboard
import os
import mouse
import threading
import seaborn

time_data = {}

def create_files():
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("user_data.json"):
        with open("user_data.json", "w") as f:
            default = {"current_date": str("14/09/2025")}
            json.dump(default, f)
    if not os.path.exists("kb_data.json"):
        with open("kb_data.json", "w") as f:
            json.dump({}, f)

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)

user_data = load_json("user_data.json")
time_data = load_json("time_data.json")
program_names = load_json("program_names.json")

def save_json(data, path):
    try:
            with open(path, "w") as f:
                json.dump(data, f)
            print("Time data succesfully saved!")
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

def get_tomorrow_date():
    tomorrow_date = datetime.date.today() + timedelta(1)
    tomorrowdatestr = tomorrow_date.strftime("%d/%m/%y")
    return tomorrowdatestr

def check_date():
    last_date = user_data.get("current_date")
    if get_date_str() > last_date:

        save_json(user_data, "user_data.json")
        time_data.clear()

        with open("time_data.json", "w") as f:
            json.dump({}, f)

check_date()

user_data = {
    "current_date": get_date_str(),
}

save_json(user_data, "user_data.json")

def gather_time_data():
    current_exe = get_foreground_exe()
    start_time = time.time()
    update_interval = 1
    save_interval = 300
    last_update = time.time()
    last_save = time.time()

    while True:
        time.sleep(1)
        new_exe = get_foreground_exe()
        now = time.time()
        check_date()
          
        self = r"C:\Users\lukar\AppData\Local\Programs\Python\Python313\python.exe"

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
            save_json(time_data, "time_data.json")
            last_save = now
        
        if new_exe == self:
            plot()

def gather_perif_data():

    mevents = []
    mouse.hook(mevents.append)
    kbevents = []
    keyboard.hook(kbevents.append)

    def process_data():

        mouse.unhook_all()
        keyboard.unhook_all()
        
        mouse_data = load_json("mouse_data.json")
        kb_data = list((load_json("kb_data.json")))
        key_counter = {}
         
        for i in mevents:
            if type(i) == mouse._mouse_event.MoveEvent or mouse._mouse_event.WheelEvent:
                pass
            else:
                if i.event_type == 'down' or i.event_type == 'double':
                    if i.button in mouse_data:
                        mouse_data[i.button] += 1
                    else:
                        mouse_data[i.button] = 1

        for i in kb_data:
            if i in key_counter:
                key_counter[i] += 1
            else:
                key_counter[i] = 1

        print(dict(sorted(key_counter.items())))

        for i in kbevents:
            if i.event_type == 'down':
                kb_data.append(i.name)

        json.dumps(kb_data)
        
        save_json(mouse_data, "mouse_data.json")
        save_json(kb_data, "kb_data.json")
        save_json(kb_data, "kb_data.json")

    keyboard.wait("esc")
    process_data()

create_files()

root = Tk()
root.title("Screentime")
root.geometry("500x500")

# class Graph(tkinter.Frame):
#     def __init__(self, master, width, height, bg):
#         self.master = master
#         self.width = width
#         self.height = height
#         self.bg = bg


graph1 = tkinter.Frame(root, width=200, height=200, bg="blue")
graph1.pack(padx=10, pady=10)

graph2 = tkinter.Frame(root, width=190, height=190, bg="red")
graph2.pack(padx=10, pady=10)

fig1 = Figure()
fig2 = Figure()

plot1 = fig1.add_subplot()
plot2 = fig2.add_subplot()

canvas1 = FigureCanvasTkAgg(figure=fig1, master = graph1)
toolbar = NavigationToolbar2Tk(canvas=canvas1, window=graph2)
canvas2 = FigureCanvasTkAgg(figure=fig2, master = graph2)
toolbar = NavigationToolbar2Tk(canvas=canvas2, window=graph2)

def plot():
    
    plot1.clear()
    plot2.clear()
    canvas1.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
    toolbar.update()
    
    mouse_data = load_json("mouse_data.json")
    kb_data = load_json("kb_data.json")
    
    final_data = {}
    for tkey, tvalue in time_data.items():
        app = os.path.basename(tkey).lower()
        app =  os.path.splitext(app)[0].lower()
        if app in program_names:
            app = program_names[app]
            final_data[app] = final_data.get(app, 0) + round(tvalue/60, 2)
        else:
            final_data[app.title()] = final_data.get(app, 0) + round(tvalue/60, 2)

    tkeys = list(final_data.keys())
    tvalues = list(final_data.values())
    plot1.bar(tkeys, tvalues)

    mkeys = list(mouse_data.keys())
    mvalues = list(mouse_data.values())
    plot2.bar(mkeys, mvalues)

    canvas1.draw()
    canvas2.draw()
    


plot_button = Button(master = root, height = 2, width = 10, text  = "Plot", command = plot)
plot_button.pack(side=TOP, anchor=NW)

thread1 = threading.Thread(target=gather_time_data)
thread1.start()
thread2 = threading.Thread(target=gather_perif_data)
thread2.start()

root.mainloop()

def exit_handler():
    save_json(time_data, "time_data.json")
    return None
atexit.register(exit_handler)