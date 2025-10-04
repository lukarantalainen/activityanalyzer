import atexit
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import plotly.express as px
import threading
import tkinter as tk
from tkinter import ttk
import loggers
import tools

def main():
    tools.check_date()

    thread1 = threading.Thread(target=loggers.record_time, daemon=True).start()
    thread2 = threading.Thread(target=loggers.record_mouse_input, daemon=True).start()
    thread3 = threading.Thread(target=loggers.record_kb_input, daemon=True).start()

    gui = Gui()
    gui.mainloop()

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen time")
        self.geometry("500x500")

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
        self.combox["values"] = ["today", "past week", "past month"]

        self.frame = GraphFrame(self, "app")
        self.add(self.frame, text="Apps")
        self.frame2 = GraphFrame(self, "mouse")
        self.add(self.frame2, text="Mouse activity")
        self.frame3 = GraphFrame(self, "kb")
        self.add(self.frame3, text="Keyboard activity")
        self.frame4 = GraphFrame(self, "net")
        self.add(self.frame4, text="Network activity")

        self.frame5 = ttk.Frame()
        self.add(self.frame5, text="Settings")

class GraphFrame(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.name = name

        self.frame = ttk.Frame(self, padding=5)
        self.fig = Figure(layout="compressed")
        self.graph = self.fig.add_subplot()

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master = self.frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()

        self.plot_btn = ttk.Button(self, text="Plot", command=self.plot_data)

        self.plot_btn.pack(ipadx=5, ipady=5)
        self.frame.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        if self.name == "mouse":
            self.text1 = tk.Text(self)
            self.text1.insert(index="end", chars="HI")
            self.text1.pack()

    def plot_data(self):
        time_data = loggers.parse_time_data()
        if self.name == "home":
            self.graph.clear()
           
            keys = list(time_data.keys())
            values = list(time_data.values())
            self.graph.pie(x=values, labels=keys)
            self.canvas.draw()

            pxfig = px.bar(time_data, x=keys, y=values)
            threading.Thread(target=pxfig.show).start()

        elif self.name == "app":
            self.graph.clear()
            time_data = loggers.parse_time_data()
            tkeys = list(time_data.keys())
            tvalues = list(time_data.values())
            self.graph.bar(tkeys, tvalues, color="cyan")
            self.canvas.draw()

        elif self.name == "mouse":
            mouse_data = loggers.parse_mouse_data()
            self.graph.clear()
            mvalues = list(mouse_data["buttons"].values())
            labels = [f"{k.capitalize()} {str(v)}" for k , v in mouse_data["buttons"].items()]
            self.graph.pie(x=mvalues, labels=labels)
            self.canvas.draw()


        elif self.name == "kb":
            kb_data = loggers.parse_kb_data()
            self.graph.clear()
            sorted_kb_data = dict(sorted(kb_data.items()))
            kbkeys = list(sorted_kb_data.keys())
            kbvalues = list(sorted_kb_data.values())
            kbkeys = [x.upper() for x in kbkeys]
            self.graph.bar(kbkeys, kbvalues, color="purple")
            self.canvas.draw()
        else:
            return None    

def exit_handler():
    loggers.save_all()
    print(">Data saved\n>Exiting...")
    return None
atexit.register(exit_handler)

main()
