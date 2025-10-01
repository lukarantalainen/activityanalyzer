
import keyboard as kb
import mouse
import os
import time
import tools
from config import TIME_DATA, MOUSE_DATA, KB_DATA, INIT_DATA


time_data = tools.load_json(TIME_DATA)
mouse_data = tools.load_json(MOUSE_DATA)
kb_data = tools.load_json(KB_DATA)
init_data = tools.load_json(INIT_DATA)
mevents = []
kbevents = []

def record_time():
    t = time.time()
    start_time = t
    last_update = t
    last_save = t
    update_interval = 1
    save_interval = 300

    while True:
        print(time_data)
        current_exe = tools.get_foreground_exe()
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
            save_all()
            tools.check_date()
            last_save = now
            
        time.sleep(1)

def record_mouse_input():
    mevents.clear()
    mouse.hook(mevents.append)

def record_kb_input():
    kbevents.clear()
    kb.hook(kbevents.append)

def parse_time_data():
    program_names = init_data
    final_data = {}
    for tkey, tvalue in time_data.items():
        app = os.path.basename(tkey).lower()
        app =  os.path.splitext(app)[0].lower()
        if app in program_names:
            app = program_names[app]
            final_data[app] = final_data.get(app, 0) + round(tvalue/60, 2)
        else:
            final_data[app.title()] = final_data.get(app, 0) + round(tvalue/60, 2)
    return final_data

def parse_mouse_data():

    mouse.unhook_all()

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

        elif type(i) == mouse._mouse_event.ButtonEvent:
            if i.event_type == "down" or i.event_type == "double":
                buttons = mouse_data["buttons"]
                try:
                    buttons[i.name] += 1
                except KeyError:
                    buttons[i.name] = 1
            mouse_data["buttons"] = buttons

        elif type(i) == mouse._mouse_event.WheelEvent:
            try:
                mouse_data["scroll_ticks"] += 1
            except KeyError:
                mouse_data["scroll_ticks"] = 1

    record_mouse_input()
    return mouse_data

def parse_kb_data():

    kb.unhook_all()

    for i in kbevents:
        key = i.name
        try:
            kb_data[key] += 1
        except KeyError:
            kb_data[key] = 1
    
    record_kb_input()
    return kb_data

def save_all():
    tools.save_json(time_data, TIME_DATA)
    tools.save_json(mouse_data, MOUSE_DATA)
    tools.save_json(kb_data, KB_DATA)

def reset_all():
    time_data.clear()
    mouse_data.clear()
    kb_data.clear()
    mevents.clear()
    kbevents.clear()