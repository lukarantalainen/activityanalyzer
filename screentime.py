import atexit
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import psutil
import seaborn as sns
import threading
import tkinter as tk
from tkinter import ttk
from config import USER_DATA, TIME_DATA, MOUSE_DATA, KB_DATA, INIT_DATA
import loggers
import tools

def main():
    tools.check_date()

    thread1 = threading.Thread(target=loggers.record_time, daemon=True)
    thread1.start()
    thread2 = threading.Thread(target=loggers.record_input, daemon=True)
    thread2.start()

    gui = Gui()
    gui.mainloop()

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
        self.button = tk.Button(self.frame01, text="Reset all")
        self.button.pack()
        self.frame01.pack()

        self.combox = ttk.Combobox(self.frame01)
        self.combox.pack()
        self.combox["values"] = ["today", "past week", "past month"]

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

        self.plot_btn.pack(anchor=tk.NW, ipadx=5, ipady=5)
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
        time_data = loggers.parse_time_data()
        if self.name == "home":
            self.graph.clear()
           
            keys = list(time_data.keys())
            values = list(time_data.values())
            self.graph.pie(x=values, labels=keys)
            self.canvas.draw()

        elif self.name == "app":
            self.graph.clear()
            time_data = loggers.parse_time_data()
            tkeys = list(time_data.keys())
            tvalues = list(time_data.values())
            self.graph.bar(tkeys, tvalues, color="cyan")
            self.canvas.draw()

        elif self.name == "mouse":
            mouse_data = loggers.process_data()[0]
            self.graph.clear()
            mkeys = list(mouse_data["buttons"].keys())
            mvalues = list(mouse_data["buttons"].values())
            self.graph.bar(mkeys, mvalues)
            self.canvas.draw()

            self.graph2.clear()
            distance = mouse_data["distance"]
            self.graph2.bar("Distance (pixels)", distance)
            self.canvas2.draw()

            self.graph3.clear()
            ticks = mouse_data["scroll_ticks"]
            print(ticks)
            self.graph3.bar("Scroll", ticks)
            self.canvas3.draw()

        elif self.name == "kb":
            kb_data = loggers.process_data()[1]
            self.graph.clear()
            sorted_kb_data = dict(sorted(kb_data.items()))
            kbkeys = list(sorted_kb_data.keys())
            kbvalues = list(sorted_kb_data.values())
            kbkeys = [x.upper() for x in kbkeys]
            self.graph.bar(kbkeys, kbvalues, color="purple")
            self.canvas.draw()
        else:
            return None

def save_all():
    tools.save_json(loggers.parse_time_data(), TIME_DATA)
    tools.save_json(loggers.process_data()[0], MOUSE_DATA)
    tools.save_json(loggers.process_data()[1], KB_DATA)
    print(">Data saved\n>Exiting...")

def exit_handler():
    save_all()
    return None
atexit.register(exit_handler)

main()
