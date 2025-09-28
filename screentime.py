import ctypes
import psutil
import time
import datetime
import atexit
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import *
from tkinter import ttk
import keyboard
import os
import mouse
import threading
import seaborn as sns
import storage
import utils

def main():
    check_date()

    thread1 = threading.Thread(target=record_time, daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=record_input, daemon=True)
    thread2.start()

    gui = Gui()
    gui.mainloop()

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

def check_date():

    user_data = utils.load_json("user_data.json")
    last_date = user_data["current_date"]

    if get_date_str() != last_date:
        utils.clear_json("time_data.json")
        utils.clear_json("mouse_data.json")
        utils.clear_json("key_counter.json")
        user_data["current_date"] = get_date_str()
        utils.save_json(user_data, "user_data.json")
    else:
        user_data["current_date"] = get_date_str()

def record_time():
    t = time.time()
    start_time = t
    last_update = t
    last_save = t
    update_interval = 1
    save_interval = 300

    while True:
        time_data = storage.time_data
        time.sleep(1)
        current_exe = get_foreground_exe()
        now = time.time()
    
        if now - last_update >= update_interval:
            elapsed_time = now - start_time
            if current_exe in time_data:
                time_data[current_exe] += round(elapsed_time)
            else:
                time_data[current_exe] = round(elapsed_time)
            start_time = now
            last_update = now

        if now - last_save >= save_interval:
            utils.save_json(time_data, "time_data.json")
            utils.save_json(storage.mouse_data, "mouse_data.json")
            utils.save_json(storage.key_counter, "key_countere.json")
            check_date()
            last_save = now

        storage.time_data = time_data

mevents = []
kbevents = []

def record_input():
    mevents.clear()
    kbevents.clear()
    mouse.hook(mevents.append)
    keyboard.hook(kbevents.append)

def process_data():
    mouse_data = storage.mouse_data
    key_counter = storage.key_counter
    buttons = mouse_data["buttons"]
    
    mouse.unhook_all()
    keyboard.unhook_all()
    for i in mevents:
        if type(i) == mouse._mouse_event.MoveEvent:
            x1 = i.x
            y1 = i.y
            break

    for i in mevents:
        
        if type(i) == mouse._mouse_event.MoveEvent:
            x2 = i.x
            y2 = i.y
            try:
                mouse_data["distance"] += (abs(x1-x2)+abs(y1-y2))
            except KeyError:
                mouse_data["distance"] = (abs(x1-x2)+abs(y1-y2))

            x1 = x2
            y1 = y2

        elif type(i) == mouse._mouse_event.WheelEvent:
            if "scroll_ticks" in mouse_data:
                mouse_data["scroll_ticks"] += 1
            else:
                mouse_data["scroll_ticks"] = 1
        else:
            if i.event_type == 'down' or i.event_type == 'double':
                if i.button in buttons:
                    buttons[i.button] += 1
                else:
                    buttons[i.button] = 1
    mouse_data["buttons"] = buttons

    for i in kbevents:
        key = i.name
        if len(key) > 5 and i.event_type != 'down':
            pass
        elif key in key_counter:
            key_counter[key] += 1
        else:
            key_counter[key] = 1
    
    storage.mouse_data = mouse_data
    storage.key_counter = key_counter

    record_input()

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen time")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tabs = GuiTabs(self)
        tabs.pack()

class GuiTabs(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        self.frame0 = ttk.Frame()
        self.add(self.frame0, text="Dashboard")
        
        

        self.frame01 = GraphFrame(self.frame0, "home")
        self.frame01.pack()

        self.combox = ttk.Combobox(self.frame01)
        self.combox.pack()
        self.combox['values'] = ['today', 'past week', 'past month']

        self.frame = GraphFrame(self, "app")
        self.add(self.frame, text="Apps")
        self.frame2 = GraphFrame(self, "mouse")
        self.add(self.frame2, text="Mouse activity")
        self.frame3 = GraphFrame(self, "kb")
        self.add(self.frame3, text="Keyboard activity")
        self.frame4 = GraphFrame(self, "net")
        self.add(self.frame4, text="Network activity")

class GraphFrame(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.name = name
        self.container = ttk.Frame(self)

        self.frame = ttk.Frame(self.container, padding=5)
        self.fig = Figure()
        self.graph = self.fig.add_subplot()

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master = self.frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()

        self.plot_btn = ttk.Button(self, text="Plot", command=self.plot_data)

        self.plot_btn.pack(anchor=NW, ipadx=5, ipady=5)
        self.container.pack(side=tk.TOP)
        self.frame.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        if self.name == "mouse":

            self.frame2 = ttk.Frame(self.container, padding=5)

            self.fig2 = Figure()
            self.graph2 = self.fig2.add_subplot()
            
            self.canvas2 = FigureCanvasTkAgg(figure=self.fig2, master = self.frame2)
            self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame2)
            self.toolbar2.update()
            self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.frame2.pack(side=tk.LEFT)

            self.frame3 = ttk.Frame(self.container, padding=5)

            self.fig3 = Figure()
            self.graph3 = self.fig3.add_subplot()

            self.canvas3 = FigureCanvasTkAgg(figure=self.fig3, master = self.frame3)
            self.toolbar3 = NavigationToolbar2Tk(self.canvas3, self.frame3)
            self.toolbar3.update()
            self.canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.frame3.pack(side=tk.LEFT)

    def plot_data(self):
        program_names = storage.program_names
        time_data = storage.time_data
        if self.name == "home":
            self.graph.clear()
            final_data = {}
            for tkey, tvalue in time_data.items():
                app = os.path.basename(tkey).lower()
                app =  os.path.splitext(app)[0].lower()
                print(app)
                if app in program_names:
                    app = program_names[app]
                    final_data[app] = final_data.get(app, 0) + round(tvalue/60, 2)
                else:
                    final_data[app.title()] = final_data.get(app, 0) + round(tvalue/60, 2)
            keys = list(final_data.keys())
            values = list(final_data.values())
            self.graph.pie(x=values, labels=keys)
            self.canvas.draw()

        elif self.name == "app":
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

        elif self.name == "mouse":
            mouse_data = storage.mouse_data
            process_data()
            self.graph.clear()
            mkeys = list(mouse_data["buttons"].keys())
            mvalues = list(mouse_data["buttons"].values())
            self.graph.pie(x=mvalues, labels=mkeys)
            self.canvas.draw()

            self.graph2.clear()
            distance = mouse_data["distance"]
            self.graph2.bar("Distance (pixels)", distance)
            self.canvas2.draw()

            self.graph3.clear()
            ticks = mouse_data["scroll_ticks"]
            self.graph3.bar("Scroll", ticks)
            self.canvas3.draw()

        elif self.name == "kb":
            key_counter = storage.key_counter
            process_data()
            self.graph.clear()
            sorted_key_counter = dict(sorted(key_counter.items()))
            kbkeys = list(sorted_key_counter.keys())
            kbvalues = list(sorted_key_counter.values())
            kbkeys = [x.upper() for x in kbkeys]
            self.graph.bar(kbkeys, kbvalues, color="purple")
            self.canvas.draw()
        else:
            return None

def save_all():
    utils.save_json(storage.time_data, "time_data.json")
    utils.save_json(storage.mouse_data, "mouse_data.json")
    utils.save_json(storage.key_counter, "key_counter.json")
    print(">Data saved\n>Exiting...")

def exit_handler():
    save_all()
    return None
atexit.register(exit_handler)

main()
