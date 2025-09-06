import json
import numpy as np
import re
import os
import win32gui
import win32ui
from PIL import Image
import matplotlib.pyplot as plt
import time

def main():
    
    if not os.path.exists("time_data.json"):
        with open("time_data.json", "w") as f:
            json.dump({}, f)

    with open("time_data.json") as f:
            tdata = json.load(f)

    with open("program_names.json") as apps:
        program_names = json.load(apps)

    def get_exe_icon(exe_path, save_path):
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        if not large:
            return None
        
        hicon = large[0]

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 64, 64)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hicon, 64, 64, 0, None, 0x3)

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        img.save(save_path)
        win32gui.DestroyIcon(hicon)

    output_dir = r"D:/VSCode/screentime/icons/"
    os.makedirs(output_dir, exist_ok=True)

    for exe_path in tdata.keys():
        match = re.search(r'[\w-]+?(?=\.)', exe_path)
        if not match:
            continue
        app_name = match.group()
        save_path = os.path.join(output_dir, app_name + ".png")
        get_exe_icon(exe_path, save_path)


    def display_data():

        final_data = {}
        for key, value in tdata.items():
            app = os.path.basename(key).lower()
            app =  os.path.splitext(app)[0].lower()
            if app in program_names:
                app = program_names[app]
                final_data[app] = final_data.get(app, 0) + round(value/60, 2)
            else:
                final_data[app.title()] = final_data.get(app, 0) + round(value/60, 2)

        keys = list(final_data.keys())
        values = list(final_data.values())

        plt.bar(keys, values)
        plt.xlabel('Applications')
        plt.ylabel('Time Spent (Minutes)')
        plt.title('Screen Time Data')
        plt.savefig("data.png")
        plt.close()
        img = Image.open("D:/VSCode/screentime/data.png")
        img.show()
        time.sleep(5)
        exit()

    display_data()