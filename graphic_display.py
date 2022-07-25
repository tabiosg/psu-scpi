import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

from power_supply import (Commands, DebugProtocol, EthernetProtocol,
                          PowerSupply, UsbProtocol)


class Application:

    app_window: tk.Tk
    volt_slider: ttk.Scale
    curr_slider: ttk.Scale
    volt_label: ttk.Label
    curr_label: ttk.Label
    power_label: ttk.Label
    on_button: ttk.Button
    protocol_button: ttk.Button
    power_supply: PowerSupply

    def __init__(self) -> None:
        self.app_window = None
        self.volt_slider = None
        self.curr_slider = None
        self.volt_label = None
        self.curr_label = None
        self.power_label = None
        self.on_button = None
        self.protocol_button = None
        self.popup_menu = None
        self.power_supply = PowerSupply(protocol=DebugProtocol())
        self.load_all_graphics()

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
        self.load_popup_menu()

    def load_popup_menu(self) -> None:
        self.popup_menu = Menu(self.app_window, tearoff=False)
        self.popup_menu.add_command(label="Change voltage resolution to 0.001", command=self.volt_res_thousandth)
        self.popup_menu.add_command(label="Change voltage resolution to 0.01", command=self.volt_res_hundredth)
        self.popup_menu.add_command(label="Change voltage resolution to 0.1", command=self.volt_res_tenths)
        self.popup_menu.add_command(label="Change voltage resolution to 1", command=self.volt_res_int)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Change current resolution to 0.001", command=self.curr_res_thousandth)
        self.popup_menu.add_command(label="Change current resolution to 0.01", command=self.curr_res_hundredth)
        self.popup_menu.add_command(label="Change current resolution to 0.1", command=self.curr_res_tenths)
        self.popup_menu.add_command(label="Change current resolution to 1", command=self.curr_res_int)
        self.app_window.bind("<Button-3>", self.popup_menu)

    def popup_menu(self, event) -> None:
        self.app_window.tk_popup(event.x_root, event.y_root)

    def volt_res_thousandth(self) -> None:
        self.volt_slider.resolution = 0.001

    def volt_res_hundredth(self) -> None:
        self.volt_slider.resolution = 0.01

    def volt_res_tenths(self) -> None:
        self.volt_slider.resolution = 0.1

    def volt_res_int(self) -> None:
        self.volt_slider.resolution = 1

    def curr_res_thousandth(self) -> None:
        self.curr_slider.resolution = 0.001

    def curr_res_hundredth(self) -> None:
        self.curr_slider.resolution = 0.01

    def curr_res_tenths(self) -> None:
        self.curr_slider.resolution = 0.1

    def curr_res_int(self) -> None:
        self.curr_slider.resolution = 1

    def load_protocol_switch(self) -> None:
        self.protocol_button = Button(text="USB", width=10, command=self.toggle_protocol_switch)
        self.protocol_button.grid(row = 3, column = 1, padx = 10, pady = 10)
        # self.protocol_button.pack(pady=10)

    def toggle_protocol_switch(self) -> None:
        # TODO - need to change this eventually to be EthernetProtocol and UsbProtocol
        if self.protocol_button.config('text')[-1] == 'USB':
            self.protocol_button.config(text='ETHERNET')
            self.power_supply = PowerSupply(protocol=DebugProtocol())
        else:
            self.protocol_button.config(text='USB')
            self.power_supply = PowerSupply(protocol=DebugProtocol())

    def load_on_switch(self) -> None:
        self.on_button = Button(text="OFF", width=10, command=self.toggle_on_switch)
        self.on_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        # self.on_button.pack(pady=10)

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
        self.volt_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.curr_label = ttk.Label(
            self.app_window,
            text=self.curr_slider.get()
        )
        self.curr_label.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.power_label = ttk.Label(
            self.app_window,
            text=self.volt_slider.get() * self.curr_slider.get()
        )
        self.power_label.grid(row = 3, column = 2, padx = 10, pady = 10)

    def load_sliders(self) -> None:
        self.volt_slider = ttk.Scale(
            self.app_window,
            from_=0,
            to=80,
            orient='horizontal',
            resolution=0.001,
            command=self.volt_slider_changed
        )
        self.volt_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.curr_slider = ttk.Scale(
            self.app_window,
            from_=0,
            to=120,
            orient='horizontal',
            resolution=0.001,
            command=self.curr_slider_changed
        )
        self.curr_slider.grid(row = 4, column = 0, padx = 10, pady = 10)

    def change_volt(self, volt: float) -> None:
        self.volt_label.configure(text=f"Voltage: {round(volt, 3)}V")
        self.power_supply.make_command(Commands.SET_VOLTS, volt)

    def volt_slider_changed(self, event) -> None:
        self.change_volt(self.volt_slider.get())
        self.update_power()

    def change_curr(self, curr: float) -> None:
        self.curr_label.configure(text=f"Current: {round(curr, 3)}A")
        self.power_supply.make_command(Commands.SET_CURR, curr)

    def curr_slider_changed(self, event) -> None:
        self.change_curr(self.curr_slider.get())
        self.update_power()

    def update_power(self) -> None:
        self.power_label.configure(
            text=f"Power: {round(self.volt_slider.get() * self.curr_slider.get(), 3)}W"
        )


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()