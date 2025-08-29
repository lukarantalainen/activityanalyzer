import json
import re
import os
import win32gui
import win32ui
from PIL import Image

with open("time_data.json") as f:
    d = json.load(f)
    
def get_exe_icon(exe_path, save_path):
    large, small = win32gui.ExtractIconEx(exe_path, 0)
    if not large:
        raise Exception("No icon found for {exe_path}")
    
    hicon = large[0]

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 64, 64)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hicon, 64, 64, 0, None, 0x3)

    # Convert to Pillow image
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

for exe_path in d.keys():
    match = re.search(r'[\w-]+?(?=\.)', exe_path)
    if not match:
        continue
    app_name = match.group()
    save_path = os.path.join(output_dir, app_name + ".png")
    try:
        get_exe_icon(exe_path, save_path)
    except Exception as e:
        print(f"Failed to get icon for {exe_path}: {e}")