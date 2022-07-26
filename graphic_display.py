import tkinter as tk
import tkinter.ttk as ttk
from random import random
from tkinter import *

from power_supply import (Commands, DebugProtocol, EthernetProtocol,
                          PowerSupply, UsbProtocol)


class Application:

    app_window: tk.Tk
    volt_frame: ttk.Frame
    curr_frame: ttk.Frame
    add_noise_frame: ttk.Frame
    mult_noise_frame: ttk.Frame
    power_frame: ttk.Frame
    volt_slider: tk.Scale
    curr_slider: tk.Scale
    add_noise_slider: tk.Scale
    mult_noise_slider: tk.Scale
    volt_label: ttk.Label
    curr_label: ttk.Label
    add_noise_label: ttk.Label
    mult_noise_label: ttk.Label
    power_label: ttk.Label
    on_button: ttk.Button
    protocol_button: ttk.Button
    popup_menu: tk.Menu
    noise_menu: tk.OptionMenu
    noise_status: tk.StringVar
    requested_voltage: float
    requested_current: float
    power_supply: PowerSupply

    def __init__(self) -> None:
        self.app_window = None
        self.volt_frame = None
        self.curr_frame = None
        self.power_frame = None
        self.add_noise_frame = None
        self.mult_noise_frame = None
        self.volt_slider = None
        self.curr_slider = None
        self.add_noise_slider = None
        self.mult_noise_slider = None
        self.volt_label = None
        self.curr_label = None
        self.add_noise_label = None
        self.mult_noise_label = None
        self.power_label = None
        self.on_button = None
        self.protocol_button = None
        self.popup_menu = None
        self.noise_menu = None
        self.noise_status = None
        self.requested_voltage = 0
        self.requested_current = 0
        self.power_supply = PowerSupply(protocol=DebugProtocol())
        self.load_all_graphics()

    def run(self) -> None:
        self.app_window.after(100, self.update_noise)
        self.app_window.mainloop()

    def center_window(self, window_name: tk.Tk) -> None:
        win_width = window_name.winfo_reqwidth()
        win_height = window_name.winfo_reqheight()
        horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
        vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
        window_name.geometry("+{}+{}".format(horiz_center, vert_center))

    def update_noise(self) -> None:
        if self.noise_status.get() == "No Noise":
            pass
        elif self.noise_status.get() == "Additive Noise":
            self.create_additive_noise(self.add_noise_slider.get())
        elif self.noise_status.get() == "Multiplicative Noise":
            self.create_mult_noise(self.mult_noise_slider.get())
        self.app_window.after(100, self.update_noise)

    def load_all_graphics(self) -> None:
        self.load_app_window()
        self.load_frames()
        self.load_sliders()
        self.load_labels()
        self.load_on_switch()
        self.load_protocol_switch()
        self.load_popup_menu()
        self.load_noise_menu()

    def load_noise_menu(self) -> None:
        choices = ["No Noise", "Additive Noise", "Multiplicative Noise"]
        self.noise_status = tk.StringVar()
        self.noise_status.set(choices[0])
        self.noise_menu = tk.OptionMenu(self.app_window, self.noise_status, *choices)
        self.noise_menu.grid(row = 0, column = 2, padx = 10, pady = 10)

    def load_popup_menu(self) -> None:
        self.popup_menu = tk.Menu(self.app_window, tearoff=False)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.001",
            command=self.volt_res_thousandth)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.01",
            command=self.volt_res_hundredth)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.1",
            command=self.volt_res_tenths)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 1",
            command=self.volt_res_int)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.001",
            command=self.curr_res_thousandth)
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.01",
            command=self.curr_res_hundredth)
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.1",
            command=self.curr_res_tenths)
        self.popup_menu.add_command(
            label="Change current slider resolution to 1",
            command=self.curr_res_int)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.001",
            command=self.add_noise_res_thousandth)
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.01",
            command=self.add_noise_res_hundredth)
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.1",
            command=self.add_noise_res_tenths)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.001",
            command=self.mult_noise_res_thousandth)
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.01",
            command=self.mult_noise_res_hundredth)
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.1",
            command=self.mult_noise_res_tenths)
        
        # Right-click
        self.app_window.bind("<Button-3>", self.show_popup_menu)

    def show_popup_menu(self, event) -> None:
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def volt_res_thousandth(self) -> None:
        self.volt_slider.configure(resolution = 0.001)

    def volt_res_hundredth(self) -> None:
        self.volt_slider.configure(resolution = 0.01)

    def volt_res_tenths(self) -> None:
        self.volt_slider.configure(resolution = 0.1)

    def volt_res_int(self) -> None:
        self.volt_slider.configure(resolution = 1)

    def curr_res_thousandth(self) -> None:
        self.curr_slider.configure(resolution = 0.001)

    def curr_res_hundredth(self) -> None:
        self.curr_slider.configure(resolution = 0.01)

    def curr_res_tenths(self) -> None:
        self.curr_slider.configure(resolution = 0.1)

    def curr_res_int(self) -> None:
        self.curr_slider.configure(resolution = 1)

    def add_noise_res_thousandth(self) -> None:
        self.add_noise_slider.configure(resolution = 0.001)

    def add_noise_res_hundredth(self) -> None:
        self.add_noise_slider.configure(resolution = 0.01)

    def add_noise_res_tenths(self) -> None:
        self.add_noise_slider.configure(resolution = 0.1)

    def mult_noise_res_thousandth(self) -> None:
        self.mult_noise_slider.configure(resolution = 0.001)

    def mult_noise_res_hundredth(self) -> None:
        self.mult_noise_slider.configure(resolution = 0.01)

    def mult_noise_res_tenths(self) -> None:
        self.mult_noise_slider.configure(resolution = 0.1)

    def load_protocol_switch(self) -> None:
        self.protocol_button = Button(text="USB", width=10, command=self.toggle_protocol_switch)
        self.protocol_button.grid(row = 1, column = 1, padx = 10, pady = 10)
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

    def toggle_on_switch(self) -> None:
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

    def load_frames(self) -> None:
        self.volt_frame = ttk.LabelFrame(
            self.app_window,
            text = "Voltage"
        )
        self.volt_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.curr_frame = ttk.LabelFrame(
            self.app_window,
            text = "Current"
        )
        self.curr_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.add_noise_frame = ttk.LabelFrame(
            self.app_window,
            text = "Additive Noise"
        )
        self.add_noise_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.mult_noise_frame = ttk.LabelFrame(
            self.app_window,
            text = "Multiplicative Noise"
        )
        self.mult_noise_frame.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.power_frame = ttk.LabelFrame(
            self.app_window,
            text = "Power"
        )
        self.power_frame.grid(row = 1, column = 2, padx = 10, pady = 10)

    def load_labels(self) -> None:
        self.volt_label = ttk.Label(
            self.volt_frame,
            text=f"Voltage: {self.volt_slider.get()} V"
        )
        self.volt_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.curr_label = ttk.Label(
            self.curr_frame,
            text=f"Curent: {self.curr_slider.get()} A"
        )
        self.curr_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.add_noise_label = ttk.Label(
            self.add_noise_frame,
            text=self.add_noise_slider.get()
        )
        self.add_noise_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.mult_noise_label = ttk.Label(
            self.mult_noise_frame,
            text=self.mult_noise_slider.get()
        )
        self.mult_noise_label.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.power_label = ttk.Label(
            self.power_frame,
            text=f"Power: {round(self.volt_slider.get() * self.curr_slider.get(), 3)} W"
        )
        self.power_label.grid(row = 0, column = 0, padx = 10, pady = 10)

    def load_sliders(self) -> None:
        self.volt_slider = tk.Scale(
            self.volt_frame,
            from_=0,
            to=80,
            orient='horizontal',
            resolution=0.001,
            command=self.volt_slider_changed
        )
        self.volt_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.curr_slider = tk.Scale(
            self.curr_frame,
            from_=0,
            to=120,
            orient='horizontal',
            resolution=0.001,
            command=self.curr_slider_changed
        )
        self.curr_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.add_noise_slider = tk.Scale(
            self.add_noise_frame,
            from_=0,
            to=1,
            orient='horizontal',
            resolution=0.001,
            command=self.add_noise_slider_changed
        )
        self.add_noise_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.mult_noise_slider = tk.Scale(
            self.mult_noise_frame,
            from_=0,
            to=0.4,
            orient='horizontal',
            resolution=0.001,
            command=self.mult_noise_slider_changed
        )
        self.mult_noise_slider.grid(row = 3, column = 0, padx = 10, pady = 10)

    def change_volt(self, volt: float) -> None:
        if (volt < 0 or volt > 80):
            return
        self.volt_label.configure(text=f"Voltage: {round(volt, 3)} V")
        self.power_supply.make_command(Commands.SET_VOLTS, volt)
        self.requested_voltage = round(volt, 3)
        self.update_power()

    def volt_slider_changed(self, event) -> None:
        self.change_volt(self.volt_slider.get())

    def change_curr(self, curr: float) -> None:
        if (curr < 0 or curr > 120):
            return
        self.curr_label.configure(text=f"Current: {round(curr, 3)} A")
        self.power_supply.make_command(Commands.SET_CURR, curr)
        self.requested_current = round(curr, 3)
        self.update_power()

    def curr_slider_changed(self, event) -> None:
        self.change_curr(self.curr_slider.get())

    def change_add_noise(self, add_noise: float) -> None:
        if(add_noise < 0 or add_noise > 1):
            return
        self.add_noise_label.configure(
            text=f"{round(add_noise, 3)}"
        )

    def add_noise_slider_changed(self, event) -> None:
        self.change_add_noise(self.add_noise_slider.get())

    def change_mult_noise(self, mult_noise: float) -> None:
        if(mult_noise < 0 or mult_noise > 0.4):
            return
        self.mult_noise_label.configure(
            text=f"{round(mult_noise, 3)}"
        )

    def mult_noise_slider_changed(self, event) -> None:
        self.change_mult_noise(self.mult_noise_slider.get())

    def update_power(self) -> None:
        self.power_label.configure(
            text=f"Power: {round(self.requested_voltage * self.requested_current, 3)} W"
        )

    def create_additive_noise(self, add_factor: float) -> None:
        self.change_volt(self.volt_slider.get() + (random() - 0.5)*add_factor)

    def create_mult_noise(self, mult_factor: float) -> None:
        # expect mult_factor to be a number between 0 and 1, most definitely closer to 0 though)
        self.change_volt(
            self.volt_slider.get()
            * (1 + (random() - 0.5)*mult_factor)
        )

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()