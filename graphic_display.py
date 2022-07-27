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
    add_volt_noise_frame: ttk.Frame
    mult_volt_noise_frame: ttk.Frame
    add_curr_noise_frame: ttk.Frame
    mult_curr_noise_frame: ttk.Frame
    power_frame: ttk.Frame
    on_frame: ttk.Frame
    protocol_frame: ttk.Frame
    noise_select_frame: ttk.Frame
    actual_frame: ttk.Frame

    volt_slider: tk.Scale
    curr_slider: tk.Scale
    power_slider: tk.Scale
    add_volt_noise_slider: tk.Scale
    mult_volt_noise_slider: tk.Scale
    add_curr_noise_slider: tk.Scale
    mult_curr_noise_slider: tk.Scale

    volt_label: ttk.Label
    curr_label: ttk.Label
    add_volt_noise_label: ttk.Label
    mult_volt_noise_label: ttk.Label
    add_curr_noise_label: ttk.Label
    mult_curr_noise_label: ttk.Label
    power_label: ttk.Label
    on_label: ttk.Label
    protocol_label: ttk.Label
    actual_voltage_label: ttk.Label
    actual_current_label: ttk.Label
    actual_power_label: ttk.Label
    constant_power_label: ttk.Label

    on_button: ttk.Button
    protocol_button: ttk.Button
    constant_power_button: ttk.Button

    popup_menu: tk.Menu
    noise_menu: tk.OptionMenu

    noise_status: tk.StringVar
    requested_voltage: float
    requested_current: float
    requested_power: float
    requested_mode_is_on: bool
    actual_voltage: float
    actual_current: float
    actual_power: float
    actual_mode: str
    constant_power: bool
    power_supply: PowerSupply

    def __init__(self) -> None:
        self.app_window = None
        self.volt_frame = None
        self.curr_frame = None
        self.power_frame = None
        self.add_volt_noise_frame = None
        self.mult_volt_noise_frame = None
        self.add_curr_noise_frame = None
        self.mult_curr_noise_frame = None
        self.on_frame = None
        self.protocol_frame = None
        self.noise_select_frame = None
        self.constant_power_frame = None
        self.volt_slider = None
        self.curr_slider = None
        self.power_slider = None
        self.add_volt_noise_slider = None
        self.mult_volt_noise_slider = None
        self.add_curr_noise_slider = None
        self.mult_curr_noise_slider = None
        self.volt_label = None
        self.curr_label = None
        self.add_volt_noise_label = None
        self.mult_volt_noise_label = None
        self.add_curr_noise_label = None
        self.mult_curr_noise_label = None
        self.power_label = None
        self.on_label = None
        self.protocol_label = None
        self.actual_voltage_label = None
        self.actual_current_label = None
        self.actual_power_label = None
        self.constant_power_label = None
        self.on_button = None
        self.protocol_button = None
        self.constant_power_button = None
        self.popup_menu = None
        self.noise_menu = None
        self.noise_status = None
        self.requested_voltage = 0
        self.requested_current = 0
        self.requested_power = 0
        self.requested_mode_is_on = False
        self.actual_voltage = 0
        self.actual_current = 0
        self.actual_power = 0
        self.constant_power = False
        self.actual_mode = "Unknown"
        self.power_supply = PowerSupply(protocol=DebugProtocol())
        self.load_all_graphics()

    def run(self) -> None:
        self.app_window.after(100, self.update_noise)
        self.app_window.after(100, self.update_actual)
        self.app_window.mainloop()

    def center_window(self, window_name: tk.Tk) -> None:
        win_width = window_name.winfo_reqwidth()
        win_height = window_name.winfo_reqheight()
        horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
        vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
        window_name.geometry("+{}+{}".format(horiz_center, vert_center))

    def update_actual(self) -> None:
        try:
            self.actual_voltage = round(float(self.power_supply.make_command(Commands.GET_VOLTS)), 3)
        except ValueError:
            # falls here since make_command for debugging is not real
            self.actual_voltage = round(random() * -1, 3)  # done for debugging purposes
        self.actual_voltage_label.configure(text=f"Voltage: {self.actual_voltage} V")
        try:
            self.actual_current = round(float(self.power_supply.make_command(Commands.GET_CURR)), 3)
        except ValueError:
            # falls here since make_command for debugging is not real
            self.actual_current = round(random() * -1, 3)  # done for debugging purposes
        self.actual_current_label.configure(text=f"Current: {self.actual_current} A")
        try:
            self.actual_power = round(self.actual_voltage * self.actual_current, 3)
        except ValueError:
            # should no longer enter here
            self.actual_power = 0
        self.actual_power_label.configure(text=f"Power: {self.actual_power} W")
        self.actual_mode = self.power_supply.make_command(Commands.GET_OUT_MODE)
        self.actual_mode_label.configure(text=f"Mode: {self.actual_mode}")
        self.app_window.after(100, self.update_actual)

    def update_noise(self) -> None:
        if not self.requested_mode_is_on:
            pass
        elif self.noise_status.get() == "None":
            pass
        elif self.noise_status.get() == "Additive":
            self.create_additive_noise()
        elif self.noise_status.get() == "Multiplicative":
            self.create_mult_noise()
        self.app_window.after(100, self.update_noise)

    def load_all_graphics(self) -> None:
        self.load_app_window()
        self.load_frames()
        self.load_sliders()
        self.load_labels()
        self.load_switches()
        self.load_popup_menu()
        self.load_noise_menu()

    def load_switches(self) -> None:
        self.on_button = Button(
            self.on_frame,
            text="Turn on",
            width=10,
            command=self.toggle_on_switch)
        self.on_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.protocol_button = Button(
            self.protocol_frame,
            text="Change to Ethernet",
            width=20,
            command=self.toggle_protocol_switch)
        self.protocol_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.constant_power_button = Button(
            self.constant_power_frame,
            text="Change to constant power",
            width=20,
            command=self.toggle_constant_power_switch)
        self.constant_power_button.grid(row = 1, column = 0, padx = 10, pady = 10)

    def load_noise_menu(self) -> None:
        choices = ["None", "Additive", "Multiplicative"]
        self.noise_status = tk.StringVar()
        self.noise_status.set(choices[0])
        self.noise_menu = tk.OptionMenu(self.noise_select_frame, self.noise_status, *choices)
        self.noise_menu.grid(row = 0, column = 0, padx = 10, pady = 10)

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
        self.add_volt_noise_slider.configure(resolution = 0.001)

    def add_noise_res_hundredth(self) -> None:
        self.add_volt_noise_slider.configure(resolution = 0.01)

    def add_noise_res_tenths(self) -> None:
        self.add_volt_noise_slider.configure(resolution = 0.1)

    def mult_noise_res_thousandth(self) -> None:
        self.mult_volt_noise_slider.configure(resolution = 0.001)

    def mult_noise_res_hundredth(self) -> None:
        self.mult_volt_noise_slider.configure(resolution = 0.01)

    def mult_noise_res_tenths(self) -> None:
        self.mult_volt_noise_slider.configure(resolution = 0.1)

    def toggle_constant_power_switch(self) -> None:
        if self.constant_power_button.config("text")[-1] == "Change to constant power":
            self.constant_power = True
            self.constant_power_label.configure(text="Currently using constant power")
            self.constant_power_button.config(text="Change to variable power")
        else:
            self.constant_power = False
            self.constant_power_label.config(text="Currently using variable power")
            self.constant_power_button.config(text="Change to constant power")

    def toggle_protocol_switch(self) -> None:
        # TODO - need to change this eventually to be EthernetProtocol and UsbProtocol
        if self.protocol_button.config("text")[-1] == "Change to USB":
            self.protocol_label.configure(text="Currently using USB")
            self.protocol_button.config(text="Change to Ethernet")
            self.power_supply = PowerSupply(protocol=DebugProtocol())
        else:
            self.protocol_label.config(text="Currently using Ethernet")
            self.protocol_button.config(text="Change to USB")
            self.power_supply = PowerSupply(protocol=DebugProtocol())

    def toggle_on_switch(self) -> None:
        if self.on_button.config("text")[-1] == "Turn on":
            self.requested_mode_is_on = True
            self.on_label.configure(text=f"Currently on")
            self.on_button.config(text="Turn off")
            self.power_supply.make_command(Commands.SET_CHANNEL_STATE, 0)
        else:
            self.requested_mode_is_on = False
            self.on_label.configure(text=f"Currently off")
            self.on_button.config(text="Turn on")
            self.power_supply.make_command(Commands.SET_CHANNEL_STATE, 1)

    def load_app_window(self) -> None:
        self.app_window = tk.Tk()
        self.app_window.title("Virtual Power Supply")

        self.center_window(self.app_window)

    def load_frames(self) -> None:
        self.volt_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Requested Voltage"
        )
        self.volt_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.curr_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Requested Current"
        )
        self.curr_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.add_volt_noise_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Additive Voltage Noise"
        )
        self.add_volt_noise_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.mult_volt_noise_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Multiplicative Voltage Noise"
        )
        self.mult_volt_noise_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.add_curr_noise_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Additive Current Noise"
        )
        self.add_curr_noise_frame.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.mult_curr_noise_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Multiplicative Current Noise"
        )
        self.mult_curr_noise_frame.grid(row = 2, column = 1, padx = 10, pady = 10)

        self.on_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Select On/Off"
        )
        self.on_frame.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.protocol_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Select Protocol"
        )
        self.protocol_frame.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.power_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Requested Power"
        )
        self.power_frame.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.noise_select_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Select Noise Type"
        )
        self.noise_select_frame.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.actual_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Actual Values"
        )
        self.actual_frame.grid(row = 0, column = 3, padx = 10, pady = 10)

        self.constant_power_frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = "Select Constant/Variable Power"
        )
        self.constant_power_frame.grid(row = 2, column = 2, padx = 10, pady = 10)

    def load_labels(self) -> None:
        self.volt_label = ttk.Label(
            self.volt_frame,
            text=f"Voltage: {self.requested_voltage} V"
        )
        self.volt_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.curr_label = ttk.Label(
            self.curr_frame,
            text=f"Curent: {self.requested_current} A"
        )
        self.curr_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.add_volt_noise_label = ttk.Label(
            self.add_volt_noise_frame,
            text=self.add_volt_noise_slider.get()
        )
        self.add_volt_noise_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.mult_volt_noise_label = ttk.Label(
            self.mult_volt_noise_frame,
            text=self.mult_volt_noise_slider.get()
        )
        self.mult_volt_noise_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.add_curr_noise_label = ttk.Label(
            self.add_curr_noise_frame,
            text=self.add_curr_noise_slider.get()
        )
        self.add_curr_noise_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.mult_curr_noise_label = ttk.Label(
            self.mult_curr_noise_frame,
            text=self.mult_curr_noise_slider.get()
        )
        self.mult_curr_noise_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.power_label = ttk.Label(
            self.power_frame,
            text=f"Power: {round(self.volt_slider.get() * self.curr_slider.get(), 3)} W"
        )
        self.power_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.on_label = ttk.Label(
            self.on_frame,
            text="Currently off"
        )
        self.on_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.protocol_label = ttk.Label(
            self.protocol_frame,
            text="Currently using USB"
        )
        self.protocol_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.actual_voltage_label = ttk.Label(
            self.actual_frame,
            text="Voltage: 0 V"
        )
        self.actual_voltage_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.actual_current_label = ttk.Label(
            self.actual_frame,
            text="Current: 0 A"
        )
        self.actual_current_label.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.actual_power_label = ttk.Label(
            self.actual_frame,
            text="Power: 0 W"
        )
        self.actual_power_label.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.actual_mode_label = ttk.Label(
            self.actual_frame,
            text="Mode: Unknown"
        )
        self.actual_mode_label.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.constant_power_label = ttk.Label(
            self.constant_power_frame,
            text="Currently using constant power"
        )
        self.constant_power_label.grid(row = 0, column = 0, padx = 10, pady = 10)

    def load_sliders(self) -> None:
        self.volt_slider = tk.Scale(
            self.volt_frame,
            from_=0,
            to=80,
            orient="horizontal",
            resolution=0.001,
            command=self.volt_slider_changed
        )
        self.volt_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.curr_slider = tk.Scale(
            self.curr_frame,
            from_=0,
            to=120,
            orient="horizontal",
            resolution=0.001,
            command=self.curr_slider_changed
        )
        self.curr_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.power_slider = tk.Scale(
            self.power_frame,
            from_=0,
            to=3000,
            orient="horizontal",
            resolution=0.001,
            command=self.power_slider_changed
        )
        self.power_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.add_volt_noise_slider = tk.Scale(
            self.add_volt_noise_frame,
            from_=0,
            to=1,
            orient="horizontal",
            resolution=0.001,
            command=self.add_volt_noise_slider_changed
        )
        self.add_volt_noise_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.mult_volt_noise_slider = tk.Scale(
            self.mult_volt_noise_frame,
            from_=0,
            to=0.4,
            orient="horizontal",
            resolution=0.001,
            command=self.mult_volt_noise_slider_changed
        )
        self.mult_volt_noise_slider.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.add_curr_noise_slider = tk.Scale(
            self.add_curr_noise_frame,
            from_=0,
            to=1,
            orient="horizontal",
            resolution=0.001,
            command=self.add_curr_noise_slider_changed
        )
        self.add_curr_noise_slider.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.mult_curr_noise_slider = tk.Scale(
            self.mult_curr_noise_frame,
            from_=0,
            to=0.4,
            orient="horizontal",
            resolution=0.001,
            command=self.mult_curr_noise_slider_changed
        )
        self.mult_curr_noise_slider.grid(row = 3, column = 0, padx = 10, pady = 10)

    def change_volt(self, volt: float) -> None:
        if (volt < 0 or volt > 80):
            return
        self.volt_label.configure(text=f"Voltage: {round(volt, 3)} V")
        self.power_supply.make_command(Commands.SET_VOLTS, volt)
        self.requested_voltage = round(volt, 3)
        self.update_power()

    def volt_slider_changed(self, event) -> None:
        previous_voltage = self.requested_voltage
        self.requested_voltage = self.volt_slider.get()
        if self.requested_voltage <= previous_voltage:
            # If we are dropping in voltage, it is safe.
            # We do this since if current is already high and voltage wants to go high,
            # we should not bump up both values until one of the values is low.
            self.change_volt(self.requested_voltage)
        if self.constant_power:
            self.requested_current = self.requested_power / self.requested_voltage
            self.change_curr(self.requested_current)
        if previous_voltage < self.requested_voltage:
            self.change_volt(self.requested_voltage)

    def change_curr(self, curr: float) -> None:
        if (curr < 0 or curr > 120):
            return
        self.curr_label.configure(text=f"Current: {round(curr, 3)} A")
        self.power_supply.make_command(Commands.SET_CURR, curr)
        self.requested_current = round(curr, 3)
        self.update_power()

    def curr_slider_changed(self, event) -> None:
        previous_current = self.requested_current
        self.requested_current = self.curr_slider.get()
        if self.requested_current <= previous_current:
            # If we are dropping in current, it is  safe.
            # We do this since if voltage is already high and current wants to go high,
            # we should not bump up both values until one of the values is low.
            self.change_curr(self.requested_current)
        if self.constant_power:
            self.requested_voltage = self.requested_power / self.requested_current
            self.change_volt(self.requested_voltage)
        if previous_current < self.requested_current:
            self.change_curr(self.requested_current)

    def power_slider_changed(self, event) -> None:
        self.requested_power = self.power_slider.get()
        if not self.constant_power:
            return
        # TODO - by default, just keep current constant and change voltage if they move the power slider.
        # but we may want to change in the future and give the user options
        self.requested_voltage = self.requested_power / self.requested_current
        self.change_volt(self.requested_voltage)

    def change_add_volt_noise(self, add_noise: float) -> None:
        if(add_noise < 0 or add_noise > 1):
            return
        self.add_volt_noise_label.configure(
            text=f"Add Volt Noise: {round(add_noise, 3)}"
        )

    def add_volt_noise_slider_changed(self, event) -> None:
        self.change_add_volt_noise(self.add_volt_noise_slider.get())

    def change_add_curr_noise(self, add_noise: float) -> None:
        if(add_noise < 0 or add_noise > 1):
            return
        self.add_curr_noise_label.configure(
            text=f"Add Curr Noise: {round(add_noise, 3)}"
        )

    def add_curr_noise_slider_changed(self, event) -> None:
        self.change_add_curr_noise(self.add_curr_noise_slider.get())

    def change_mult_volt_noise(self, mult_noise: float) -> None:
        if(mult_noise < 0 or mult_noise > 0.4):
            return
        self.mult_volt_noise_label.configure(
            text=f"{round(mult_noise, 3)}"
        )

    def mult_volt_noise_slider_changed(self, event) -> None:
        self.change_mult_volt_noise(self.mult_volt_noise_slider.get())

    def change_mult_curr_noise(self, mult_noise: float) -> None:
        if(mult_noise < 0 or mult_noise > 0.4):
            return
        self.mult_curr_noise_label.configure(
            text=f"Mult Curr Noise: {round(mult_noise, 3)}"
        )

    def mult_curr_noise_slider_changed(self, event) -> None:
        self.change_mult_curr_noise(self.mult_curr_noise_slider.get())        

    def update_power(self) -> None:
        self.power_label.configure(
            text=f"Power: {round(self.requested_voltage * self.requested_current, 3)} W"
        )

    def create_additive_noise(self) -> None:
        add_volt_factor = self.add_volt_noise_slider.get()
        self.change_volt(self.requested_voltage + (random() - 0.5)*add_volt_factor)

        add_curr_factor = self.add_curr_noise_slider.get()
        self.change_curr(self.requested_current + (random() - 0.5)*add_curr_factor)

    def create_mult_noise(self) -> None:
        mult_volt_factor = self.mult_volt_noise_slider.get()
        # expect mult_factor to be a number between 0 and 1, most definitely closer to 0 though)
        self.change_volt(
            self.requested_voltage
            * (1 + (random() - 0.5)*mult_volt_factor)
        )

        mult_curr_factor = self.mult_curr_noise_slider.get()
        self.change_curr(
            self.requested_current
            * (1 + (random() - 0.5)*mult_curr_factor)
        )

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()