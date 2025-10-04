import atexit
import plotly.express as px
import threading
import loggers
import tools
import pandas as pd
from config import MAIN_HTML

def main():
    tools.check_date()

    thread1 = threading.Thread(target=loggers.record_time, daemon=True).start()
    thread2 = threading.Thread(target=loggers.record_mouse_input, daemon=True).start()
    thread3 = threading.Thread(target=loggers.record_kb_input, daemon=True).start()
    listener()

def listener():    
    x = 0
    def plot_data(num: int = 0):

        if num == 1:
            time_data = pd.DataFrame(loggers.parse_time_data().items())
            fig = px.bar(time_data, x=0, y=1)
            fig.show()
            print(time_data)                        

        elif num == 2:
            mouse_data = loggers.parse_mouse_data()
            buttons = pd.DataFrame(list(mouse_data.get("buttons", {"middle": 0}).items()))

            fig = px.bar(buttons, x=0, y=1)
            fig.show()


        elif num == 3:
            kb_data = pd.DataFrame(loggers.parse_kb_data().items())
            fig = px.bar(kb_data, x=0, y=1)
            fig.write_html(MAIN_HTML)
            fig.show()

    try:
        x = int(input("Type '1' for time Type '2' for mouse Type '3' for keyboard: "))
    except ValueError:
        print("Invalid input")
    plot_data(x)

    listener()

def exit_handler():
    loggers.save_all()
    print(">Data saved\n>Exiting...")
    return None
atexit.register(exit_handler)

main()
