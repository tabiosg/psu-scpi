import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

from power_supply import (Commands, DebugProtocol, EthernetProtocol,
                          PowerSupply, UsbProtocol)


class Application:

    def __init__(self) -> None:
        self.load_all_graphics()
        self.app_window = None
        self.volt_slider = None
        self.curr_slider = None
        self.volt_label = None
        self.curr_label = None
        self.power_label = None
        self.on_button = None
        self.protocol_button = None
        self.power_supply = PowerSupply(protocol=DebugProtocol())

    def run(self) -> None:
        self.app_window.mainloop()

    def center_window(self, window_name: tk.Tk) -> None:
        win_width = window_name.winfo_reqwidth()
        win_height = window_name.winfo_reqheight()
        horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
        vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
        window_name.geometry("+{}+{}".format(horiz_center, vert_center))

    def load_all_graphics(self) -> None:
        self.load_app_window()
        self.load_sliders()
        self.load_labels()
        self.load_on_switch()
        self.load_protocol_switch()

    def load_protocol_switch(self) -> None:
        self.protocol_button = Button(text="USB", width=10, command=self.toggle_protocol_switch)
        self.protocol_button.pack(pady=10)

    def toggle_protocol_switch(self) -> None:
        # TODO - need to change this eventually to be EthernetProtocol and UsbProtocol
        if self.on_button.config('text')[-1] == 'USB':
            self.on_button.config(text='ETHERNET')
            self.power_supply = PowerSupply(protocol=DebugProtocol())
        else:
            self.on_button.config(text='USB')
            self.power_supply = PowerSupply(protocol=DebugProtocol())

    def load_on_switch(self) -> None:
        self.on_button = Button(text="OFF", width=10, command=self.toggle_on_switch)
        self.on_button.pack(pady=10)

    def toggle_on_switch(self) -> None:
        # TODO - verify if this works
        if self.on_button.config('text')[-1] == 'ON':
            self.on_button.config(text='OFF')
            self.power_supply.make_command(Commands.SET_CHANNEL_STATE, 0)
        else:
            self.on_button.config(text='ON')
            self.power_supply.make_command(Commands.SET_CHANNEL_STATE, 1)

    def load_app_window(self) -> None:
        self.app_window = tk.Tk()
        self.app_window.title("Virtual Power Supply")
        self.center_window(self.app_window)

    def load_labels(self) -> None:
        self.volt_label = ttk.Label(
            self.app_window,
            text=self.volt_slider.get()
        )
        self.curr_label = ttk.Label(
            self.app_window,
            text=self.curr_slider.get()
        )
        self.power_label = ttk.Label(
            self.app_window,
            text=self.volt_slider.get() * self.curr_slider.get()
        )

    def load_sliders(self) -> None:
        self.volt_slider = ttk.Scale(
            self.app_window,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.volt_slider_changed
        )
        self.curr_slider = ttk.Scale(
            self.app_window,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.curr_slider_changed
        )

    def change_volt(self, volt: float) -> None:
        self.volt_label.configure(text=volt)
        self.power_supply.make_command(Commands.SET_VOLTS, volt)

    def volt_slider_changed(self, event) -> None:
        
        self.change_volt(self.volt_slider.get())
        self.update_power()

    def change_curr(self, curr: float) -> None:
        self.curr_label.configure(text=curr)
        self.power_supply.make_command(Commands.SET_CURR, curr)

    def curr_slider_changed(self, event) -> None:
        self.change_curr(self.volt_slider.get())
        self.update_power()

    def update_power(self) -> None:
        self.power_label.configure(
            text=self.volt_slider.get() * self.curr_slider.get()
        )


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()