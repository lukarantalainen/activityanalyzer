
import keyboard
import mouse
import os
import time
import tools
from config import TIME_DATA, MOUSE_DATA, KB_DATA, INIT_DATA

time_data = tools.load_json(TIME_DATA)
mouse_data = tools.load_json(MOUSE_DATA)
kb_data = tools.load_json(KB_DATA)
init_data = tools.load_json(INIT_DATA)

def record_time():
    t = time.time()
    start_time = t
    last_update = t
    last_save = t
    update_interval = 1
    save_interval = 300

    while True:
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

mevents = []
kbevents = []

def record_input():
    mevents.clear()
    kbevents.clear()
    mouse.hook(mevents.append)
    keyboard.hook(kbevents.append)

def process_data():
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
            if i.event_type == "down" or i.event_type == "double":
                if i.button in buttons:
                    buttons[i.button] += 1
                else:
                    buttons[i.button] = 1
    mouse_data["buttons"] = buttons

    for i in kbevents:
        key = i.name
        if len(key) > 5 and i.event_type != "down":
            pass
        elif key in kb_data:
            kb_data[key] += 1
        else:
            kb_data[key] = 1

    record_input()
    return mouse_data, kb_data

def save_all():
    tools.save_json(time_data, TIME_DATA)
    tools.save_json(mouse_data, MOUSE_DATA)
    tools.save_json(kb_data, KB_DATA)

