import tkinter as tk
import tkinter.ttk as ttk
from random import random
from tkinter import *
from typing import Callable

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
    noise_select_frame: ttk.Frame
    actual_frame: ttk.Frame
    on_frame: ttk.Frame
    protocol_frame: ttk.Frame
    voltage_current_constant_frame: ttk.Frame

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
    voltage_current_constant_label: ttk.Label

    on_button: ttk.Button
    protocol_button: ttk.Button
    constant_power_button: ttk.Button
    voltage_current_constant_button: ttk.Button

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
    constant_voltage: bool
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
        self.voltage_current_constant_frame = None
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
        self.voltage_current_constant_label = None
        self.on_button = None
        self.protocol_button = None
        self.constant_power_button = None
        self.voltage_current_constant_button = None
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
        self.constant_voltage = True
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
            self.actual_voltage = float(self.power_supply.make_command(Commands.GET_VOLTS)), 3
        except ValueError:
            # falls here since make_command for debugging is not real
            self.actual_voltage = round(random() * -1, 3)  # done for debugging purposes
        self.actual_voltage_label.configure(text=f"Voltage: {round(self.actual_voltage, 3)} V")
        try:
            self.actual_current = float(self.power_supply.make_command(Commands.GET_CURR)), 3
        except ValueError:
            # falls here since make_command for debugging is not real
            self.actual_current = round(random() * -1, 3)  # done for debugging purposes
        self.actual_current_label.configure(text=f"Current: {round(self.actual_current, 3)} A")
        try:
            self.actual_power = self.actual_voltage * self.actual_current
        except ValueError:
            # should no longer enter here
            self.actual_power = 0
        self.actual_power_label.configure(text=f"Power: {round(self.actual_power, 3)} W")
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

    def create_switch(self, frame: ttk.Frame, text: str, cmd: Callable) -> ttk.Button:
        button = Button(
            frame,
            text=text,
            width=10,
            command=cmd)
        button.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "NSEW")
        return button

    def load_switches(self) -> None:
        self.on_button = self.create_switch(self.on_frame, "Turn on", self.toggle_on_switch)
        self.protocol_button = self.create_switch(self.protocol_frame, "Change to Ethernet", self.toggle_protocol_switch)
        self.constant_power_button = self.create_switch(self.constant_power_frame, "Change to constant power", self.toggle_constant_power_switch)
        self.voltage_current_constant_button = self.create_switch(self.voltage_current_constant_frame, "Change to constant current", self.toggle_voltage_current_constant_switch)

    def load_noise_menu(self) -> None:
        choices = ["None", "Additive", "Multiplicative"]
        self.noise_status = tk.StringVar()
        self.noise_status.set(choices[0])
        self.noise_menu = tk.OptionMenu(self.noise_select_frame, self.noise_status, *choices)
        self.noise_menu.grid(row = 0, column = 0, padx = 10, pady = 10)

    def load_popup_menu(self) -> None:
        self.popup_menu = tk.Menu(self.app_window, tearoff=False)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 1",
            command=self.volt_res_int)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.1",
            command=self.volt_res_tenths)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.01",
            command=self.volt_res_hundredth)
        self.popup_menu.add_command(
            label="Change voltage slider resolution to 0.001",
            command=self.volt_res_thousandth)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change current slider resolution to 1",
            command=self.curr_res_int)
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.1",
            command=self.curr_res_tenths)
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.01",
            command=self.curr_res_hundredth)
        self.popup_menu.add_command(
            label="Change current slider resolution to 0.001",
            command=self.curr_res_thousandth)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.1",
            command=self.add_noise_res_tenths)
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.01",
            command=self.add_noise_res_hundredth)
        self.popup_menu.add_command(
            label="Change add noise slider resolution to 0.001",
            command=self.add_noise_res_thousandth)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.1",
            command=self.mult_noise_res_tenths)
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.01",
            command=self.mult_noise_res_hundredth)
        self.popup_menu.add_command(
            label="Change mult noise slider resolution to 0.001",
            command=self.mult_noise_res_thousandth)
        
        self.app_window.bind("<Button-3>", self.show_popup_menu)

    def show_popup_menu(self, event) -> None:
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def change_slider_resolution(self, slider: tk.Scale, res: float) -> None:
        slider.configure(resolution=res)

    def volt_res_thousandth(self) -> None:
        self.change_slider_resolution(self.volt_slider, 0.001)

    def volt_res_hundredth(self) -> None:
        self.change_slider_resolution(self.volt_slider, 0.01)

    def volt_res_tenths(self) -> None:
        self.change_slider_resolution(self.volt_slider, 0.1)

    def volt_res_int(self) -> None:
        self.change_slider_resolution(self.volt_slider, 1)

    def curr_res_thousandth(self) -> None:
        self.change_slider_resolution(self.curr_slider, 0.001)

    def curr_res_hundredth(self) -> None:
        self.change_slider_resolution(self.curr_slider, 0.01)

    def curr_res_tenths(self) -> None:
        self.change_slider_resolution(self.curr_slider, 0.1)

    def curr_res_int(self) -> None:
        self.change_slider_resolution(self.curr_slider, 1)

    def add_noise_res_thousandth(self) -> None:
        self.change_slider_resolution(self.add_volt_noise_slider, 0.001)

    def add_noise_res_hundredth(self) -> None:
        self.change_slider_resolution(self.add_volt_noise_slider, 0.01)

    def add_noise_res_tenths(self) -> None:
        self.change_slider_resolution(self.add_volt_noise_slider, 0.1)

    def mult_noise_res_thousandth(self) -> None:
        self.change_slider_resolution(self.mult_volt_noise_slider, 0.001)

    def mult_noise_res_hundredth(self) -> None:
        self.change_slider_resolution(self.mult_volt_noise_slider, 0.01)

    def mult_noise_res_tenths(self) -> None:
        self.change_slider_resolution(self.mult_volt_noise_slider, 0.1)

    def toggle_voltage_current_constant_switch(self) -> None:
        if self.voltage_current_constant_button.config("text")[-1] == "Change to constant current":
            self.constant_voltage = False
            self.voltage_current_constant_label.configure(text="Currently using constant current")
            self.voltage_current_constant_button.config(text="Change to constant voltage")
        else:
            self.constant_voltage = True
            self.voltage_current_constant_label.config(text="Currently using constant voltage")
            self.voltage_current_constant_button.config(text="Change to constant current")

    def toggle_constant_power_switch(self) -> None:
        if self.constant_power_button.config("text")[-1] == "Change to constant power":
            self.constant_power = True
            self.constant_power_label.configure(text="Currently using constant power")
            self.power_slider.pack()
            self.constant_power_button.config(text="Change to variable power")
        else:
            self.constant_power = False
            self.constant_power_label.config(text="Currently using variable power")
            self.power_slider.pack_forget()
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

    def create_frame(self, text: str, row: int, col: int) -> ttk.Frame:
        frame = ttk.LabelFrame(
            self.app_window,
            width = 150,
            text = text
        )
        frame.grid(row=row, column=col, padx=10, pady=10)
        return frame

    def load_frames(self) -> None:
        self.volt_frame = self.create_frame("Requested Voltage", 0, 0)
        self.curr_frame = self.create_frame("Requested Current", 0, 1)
        self.noise_select_frame = self.create_frame("Select Noise Type", 0, 2)
        self.actual_frame = self.create_frame("Actual Values", 0, 3)
        self.add_volt_noise_frame = self.create_frame("Additive Voltage Noise", 1, 0)
        self.add_curr_noise_frame = self.create_frame("Additive Current Noise", 1, 1)
        self.power_frame = self.create_frame("Requested Power", 1, 2)
        self.mult_volt_noise_frame = self.create_frame("Multiplicative Voltage Noise", 2, 0)
        self.mult_curr_noise_frame = self.create_frame("Multiplicative Current Noise", 2, 1)
        self.constant_power_frame = self.create_frame("Select Constant/Variable Power", 2, 2)
        self.on_frame = self.create_frame("Select On/Off", 3, 0)
        self.protocol_frame = self.create_frame("Select Protocol", 3, 1)
        self.voltage_current_constant_frame = self.create_frame("Keep Voltage/Current Constant When Changing Power", 3, 2)

    def create_label(self, frame: tk.Frame, text: str, row: int) -> ttk.Label:
        label = ttk.Label(
            frame,
            text=text
        )
        label.grid(row=row, column=0, padx=10, pady=10)
        return label

    def load_labels(self) -> None:
        self.volt_label = self.create_label(self.volt_frame, "Voltage: 0 V", 0)
        self.curr_label = self.create_label(self.curr_frame, "Curent: 0 A", 0)
        self.add_volt_noise_label = self.create_label(self.add_volt_noise_frame, "Add Volt Noise: 0", 0)
        self.mult_volt_noise_label = self.create_label(self.mult_volt_noise_frame, "Mult Volt Noise: 0", 0)
        self.add_curr_noise_label = self.create_label(self.add_curr_noise_frame, "Add Curr Noise: 0", 0)
        self.mult_curr_noise_label = self.create_label(self.mult_curr_noise_frame, "Mult Curr Noise: 0", 0)
        self.power_label = self.create_label(self.power_frame, "Power: 0 W", 0)
        self.on_label = self.create_label(self.on_frame, "Currently off", 0)
        self.protocol_label = self.create_label(self.protocol_frame, "Currently using USB", 0)
        self.actual_voltage_label = self.create_label(self.actual_frame, "Voltage: 0 V", 0)
        self.actual_current_label = self.create_label(self.actual_frame, "Current: 0 A", 1)
        self.actual_power_label = self.create_label(self.actual_frame, "Power: 0 W", 2)
        self.actual_mode_label = self.create_label(self.actual_frame, "Mode: Unknown", 3)
        self.constant_power_label = self.create_label(self.constant_power_frame, "Currently using constant power", 0)
        self.voltage_current_constant_label = self.create_label(self.voltage_current_constant_frame, "Currently using constant voltage", 0)

    def create_slider(self, frame: ttk.Frame, max: float, cmd: Callable) -> tk.Scale:
        slider = tk.Scale(
            frame,
            from_=0,
            to=max,
            orient="horizontal",
            resolution=0.001,
            command=cmd
        )
        slider.grid(row = 1, column = 0, padx = 10, pady = 10)
        return slider

    def load_sliders(self) -> None:
        self.volt_slider = self.create_slider(self.volt_frame, 80, self.volt_slider_changed)
        self.curr_slider = self.create_slider(self.curr_frame, 120, self.curr_slider_changed)
        self.power_slider = self.create_slider(self.power_frame, 3000, self.power_slider_changed)
        self.power_slider.pack_forget()
        self.add_volt_noise_slider = self.create_slider(self.add_volt_noise_frame, 1, self.add_volt_noise_slider_changed)
        self.mult_volt_noise_slider = self.create_slider(self.mult_volt_noise_frame, 0.4, self.mult_volt_noise_slider_changed)
        self.add_curr_noise_slider = self.create_slider(self.add_curr_noise_frame, 1, self.add_curr_noise_slider_changed)
        self.mult_curr_noise_slider = self.create_slider(self.mult_curr_noise_frame, 0.4, self.mult_curr_noise_slider_changed)

    def change_volt(self, volt: float) -> None:
        if (volt < 0 or volt > 80):
            return
        volt = min(
            volt,
            3000.0 / self.requested_current if self.requested_current != 0 
            else volt
        )
        self.volt_label.configure(text=f"Voltage: {round(volt, 3)} V")
        self.power_supply.make_command(Commands.SET_VOLTS, volt)
        self.requested_voltage = volt
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
            self.requested_current = (
                self.requested_power / self.requested_voltage if self.requested_voltage != 0
                else 0
            )
            self.change_curr(self.requested_current)
        if previous_voltage < self.requested_voltage:
            self.change_volt(self.requested_voltage)

    def change_curr(self, curr: float) -> None:
        if (curr < 0 or curr > 120):
            return
        curr = min(
            curr,
            3000.0 / self.requested_voltage if self.requested_voltage != 0 
            else curr
        )
        self.curr_label.configure(text=f"Current: {round(curr, 3)} A")
        self.power_supply.make_command(Commands.SET_CURR, curr)
        self.requested_current = curr
        self.update_power()

    def curr_slider_changed(self, event) -> None:
        previous_current = self.requested_current
        self.requested_current = self.curr_slider.get()
        if self.requested_current <= previous_current:
            # If we are dropping in current, it is safe.
            # We do this since if voltage is already high and current wants to go high,
            # we should not bump up both values until one of the values is low.
            self.change_curr(self.requested_current)
        if self.constant_power:
            self.requested_voltage = (
                self.requested_power / self.requested_current if self.requested_current != 0
                else 0
            )
            self.change_volt(self.requested_voltage)
        if previous_current < self.requested_current:
            self.change_curr(self.requested_current)

    def power_slider_changed(self, event) -> None:
        self.requested_power = self.power_slider.get()
        if not self.constant_power:
            return
        if self.constant_voltage:
            self.requested_current = (
                self.requested_power / self.requested_voltage if self.requested_voltage != 0
                else 0
            )
            self.change_volt(self.requested_current)
        if not self.constant_voltage:
            self.requested_voltage = (
                self.requested_power / self.requested_current if self.requested_current != 0
                else 0
            )
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