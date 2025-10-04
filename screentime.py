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

    def plot_data(self):
        
        if self.name == "home":
            time_data = loggers.parse_time_data()


        elif self.name == "app":
            time_data = loggers.parse_time_data()


        elif self.name == "mouse":
            mouse_data = loggers.parse_mouse_data()
            


        elif self.name == "kb":
            kb_data = loggers.parse_kb_data()

def exit_handler():
    loggers.save_all()
    print(">Data saved\n>Exiting...")
    return None
atexit.register(exit_handler)

main()
