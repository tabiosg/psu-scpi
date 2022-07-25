import tkinter as tk
import tkinter.ttk as ttk

from power_supply import Commands, DebugProtocol, PowerSupply


class Application:

    def __init__(self) -> None:
        self.load_all_graphics()

    def center_window(self, window_name: tk.Tk) -> None:
        win_width = window_name.winfo_reqwidth()
        win_height = window_name.winfo_reqheight()
        horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
        vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
        window_name.geometry("+{}+{}".format(horiz_center, vert_center))

    def load_all_graphics(self) -> None:
        self.load_app_window()
        self.load_display_boxes()
        self.load_sliders()
        self.load_on_switch()
        self.load_protocol_switch()

    def load_app_window(self) -> None:
        app_window = tk.Tk()
        app_window.title("Virtual Power Supply")
        self.center_window(app_window)


def main():
    app = Application()

if __name__ == "__main__":
    main()