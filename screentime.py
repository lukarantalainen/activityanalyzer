import ctypes
import psutil
import time
import datetime
from datetime import timedelta
import atexit
import json
from matplotlib.figure import Figure
from tkinter import *
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import Image
import keyboard
import os
import mouse
import threading

time_data = {}

def create_files():
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("user_data.json"):
        with open("user_data.json", "w") as f:
            default = {"current_date": str("14/09/2025")}
            json.dump(default, f)

create_files()

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
    except IOError:
        print("An IOError has occured.")



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

        if new_exe == self:
            plot()

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

def gather_mouse_data():

    events = []
    mouse.hook(events.append)
 
    def process_data():

        mouse.unhook_all()

        mouse_data = {}


        if not os.path.exists("mouse_data.json"):
            
            mouse_data = {
                "mouse1": 0, #lclick
                "mouse2": 0, #rclick
                "mouse3": 0, #back
                "mouse4": 0 #forward
 
            }

            save_json(mouse_data, "mouse_data.json")
        

        mouse_data = load_json("mouse_data.json")

        move_data = []
        
        for i in events:
            print(i.button)

        # for item in events:
        #     if item.button=='left' and item.event_type=='down':
        #         mouse_data["mouse1"] += 1
        #     elif str(item).startswith("ButtonEvent(event_type='down', button='left'")==True:
        #         mouse_data["mouse1"] += 2
        #         print("hello")
        #     if str(item).startswith("ButtonEvent(event_type='double', button='right'")==True:
        #       mouse_data["mouse2"] +=1
        #     elif str(item).startswith("ButtonEvent(event_type='down', button='right'")==True:
        #       mouse_data["mouse2"] +=2
        #     if str(item).startswith("ButtonEvent(event_type='double', button='x'")==True:
        #       mouse_data["mouse3"] +=1
        #     elif str(item).startswith("ButtonEvent(event_type='down', button='x'")==True:
        #       mouse_data["mouse3"] +=2
        #     if str(item).startswith("ButtonEvent(event_type='double', button='x2'")==True:
        #       mouse_data["mouse4"] +=1
        #     elif str(item).startswith("ButtonEvent(event_type='down', button='x2'")==True:
        #         mouse_data["mouse4"] +=1

        #     if str(item).startswith("MoveEvent"):
        #         move_data.append(item)
                



        save_json(mouse_data, "mouse_data.json")

        mouse.play(move_data)
 
    keyboard.wait("space")
    process_data()


root = Tk()
root.title("Screentime")
root.geometry("500x500")

fig1 = Figure(figsize=(10,10), dpi = 100)
fig2 = Figure(figsize=(10,10), dpi = 100)

plot1 = fig1.add_subplot()
plot2 = fig2.add_subplot()

canvas = FigureCanvasTkAgg(fig1, master = root)
toolbar = NavigationToolbar2Tk(canvas, root)



def plot():

    mouse_data = load_json("mouse_data.json")
    
    plot1.clear()
    plot2.clear()
    canvas.get_tk_widget().pack()
    toolbar.update()
    
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

    canvas.draw()
    


    



plot_button = Button(master = root, height = 2, width = 10, text  = "Plot", command = plot)
plot_button.pack(side=TOP, anchor=NW)

thread1 = threading.Thread(target=gather_time_data)
thread1.start()
thread2 = threading.Thread(target=gather_mouse_data)
thread2.start()

root.mainloop()




def exit_handler():
    save_json(time_data, "time_data.json")
    return None
atexit.register(exit_handler)