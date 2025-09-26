import ctypes
import psutil
import time
import datetime
from datetime import timedelta
import atexit
import json
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import keyboard
import os
import mouse
import threading
import seaborn
from PIL import Image, ImageTk

def main():
    create_files()
    check_date()

    global time_data, mouse_data, kb_data, key_counter
    time_data = load_json("time_data.json")
    mouse_data = load_json("mouse_data.json")
    kb_data = list(load_json("kb_data.json"))
    key_counter = {}

    thread1 = threading.Thread(target=record_time, daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=record_input, daemon=True)
    thread2.start()

    gui = Gui()
    gui.mainloop()

def create_files():
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("user_data.json"):
        with open("user_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("kb_data.json"):
        with open("kb_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("mouse_data.json"):
        with open("mouse_data.json", "w") as f:
            json.dump({}, f)

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)

def clear_json(path):
    with open(path, "w") as f:
        json.dump({}, f)

def save_json(data, path):
    try:
            with open(path, "w") as f:
                json.dump(data, f)
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
    user_data = load_json("user_data.json")
    last_date = user_data["current_date"]
    if get_date_str() != last_date:
        clear_json("time_data.json")
        clear_json("mouse_data.json")
        clear_json("kb_data.json")
        user_data["current_date"] = get_date_str()
        save_json(user_data, "user_data.json")
    else:
        user_data["current_date"] = get_date_str()

def record_time():
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
            check_date()
            last_save = now
mevents = []
kbevents = []

def record_input():
    mevents.clear()
    kbevents.clear()
    mouse.hook(mevents.append)
    keyboard.hook(kbevents.append)

def process_data():
    mouse.unhook_all()
    keyboard.unhook_all()

    for i in mevents:
        if type(i) == mouse._mouse_event.MoveEvent:
            pass
        elif type(i) == mouse._mouse_event.WheelEvent:
            print(i)
        else:
            if i.event_type == 'down' or i.event_type == 'double':
                if i.button in mouse_data:
                    mouse_data[i.button] += 1
                else:
                    mouse_data[i.button] = 1

    for i in kbevents:
        if i.event_type == 'down':
            kb_data.append(i.name)

    for i in kb_data:
        if i in key_counter:
            key_counter[i] += 1
        else:
            key_counter[i] = 1

    save_json(mouse_data, "mouse_data.json")
    json.dumps(kb_data)
    save_json(kb_data, "kb_data.json")
    
    record_input()

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screentime")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tabs = GuiTabs()
        tabs.grid(column=0, row=0)

class GuiTabs(ttk.Notebook):
    def __init__(self):
        super().__init__()
        frame0 = ttk.Frame(self)
        text = tk.Text(frame0)
        text.insert("1.0", "Home")
        text.pack()
        self.add(frame0, text="Home")
        frame = GraphFrame(self, "Time data")
        self.add(frame, text="Time data")
        frame2 = GraphFrame(self, "Mouse data")
        self.add(frame2, text="Mouse data")
        frame3 = GraphFrame(self, "Keyboard data")
        self.add(frame3, text="Keyboard data")

class GraphFrame(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)

        
        self.name = name

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.graph = self.fig.add_subplot()

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master = self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        

        # self.refresh_icon =  tk.PhotoImage(file=img)

        self.plot_btn = ttk.Button(self, text="Plot", command=self.plot_data)

        self.plot_btn.pack(side=tk.BOTTOM, ipadx=5, ipady=5)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def plot_data(self):

        if self.name == "Time data":
            program_names = load_json("program_names.json")
            self.graph.clear()
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
            self.graph.bar(tkeys, tvalues, color="cyan")
            self.canvas.draw()

        elif self.name == "Mouse data":
            process_data()
            self.graph.clear()
            mkeys = list(mouse_data.keys())
            mvalues = list(mouse_data.values())
            self.graph.bar(mkeys, mvalues, color="yellow")
            self.canvas.draw()

        elif self.name == "Keyboard data":
            process_data()
            self.graph.clear()
            
            kbkeys = list(key_counter.keys())
            kbvalues = list(key_counter.values())
            self.graph.stem(kbkeys, kbvalues)
            key_counter.clear()
            self.canvas.draw() 
        else:
            return None

def save_all():
    save_json(time_data, "time_data.json")
    save_json(mouse_data, "mouse_data.json")
    save_json(kb_data, "kb_data.json")
    print(">Data saved\n>Exiting...")

def exit_handler():
    save_all()
    return None
atexit.register(exit_handler)

main()