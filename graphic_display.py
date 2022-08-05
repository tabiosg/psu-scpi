import tkinter as tk
import tkinter.ttk as ttk
from random import random
from tkinter import *
from typing import Callable

from power_supply import (Commands, DebugProtocol, EthernetProtocol,
                          PowerSupply, UsbProtocol)


class Application:

    _app_window: tk.Tk
    
    _actual_frame: ttk.LabelFrame
    _add_curr_noise_frame: ttk.LabelFrame
    _add_volt_noise_frame: ttk.LabelFrame
    _curr_frame: ttk.LabelFrame
    _excel_frame: ttk.LabelFrame
    _max_frame: ttk.LabelFrame
    _mult_curr_noise_frame: ttk.LabelFrame
    _mult_volt_noise_frame: ttk.LabelFrame
    _noise_select_frame: ttk.LabelFrame
    _power_frame: ttk.LabelFrame
    _on_frame: ttk.LabelFrame
    _protocol_frame: ttk.LabelFrame
    _volt_frame: ttk.LabelFrame
    _volt_curr_constant_frame: ttk.LabelFrame

    _volt_slider: tk.Scale
    _curr_slider: tk.Scale
    _power_slider: tk.Scale
    _add_volt_noise_slider: tk.Scale
    _add_curr_noise_slider: tk.Scale
    _max_curr_slider: tk.Scale
    _max_power_slider: tk.Scale
    _max_volt_slider: tk.Scale
    _mult_curr_noise_slider: tk.Scale
    _mult_volt_noise_slider: tk.Scale

    _volt_label: ttk.Label
    _curr_label: ttk.Label
    _add_volt_noise_label: ttk.Label
    _mult_volt_noise_label: ttk.Label
    _add_curr_noise_label: ttk.Label
    _mult_curr_noise_label: ttk.Label
    _power_label: ttk.Label
    _on_label: ttk.Label
    _protocol_label: ttk.Label
    _actual_voltage_label: ttk.Label
    _actual_current_label: ttk.Label
    _actual_power_label: ttk.Label
    _constant_power_label: ttk.Label
    _volt_curr_constant_label: ttk.Label

    _constant_power_button: tk.Button
    _excel_button: tk.Button
    _on_button: tk.Button
    _protocol_button: tk.Button
    _volt_curr_constant_button: tk.Button

    _popup_menu: tk.Menu
    _noise_menu: tk.OptionMenu

    _max_current: float
    _max_voltage: float
    _max_power: float
    _requested_voltage: float
    _requested_current: float
    _requested_power: float

    _constant_power: bool
    _constant_voltage: bool
    _requested_mode_is_on: bool

    _noise_status: tk.StringVar

    _actual_current: float
    _actual_power: float
    _actual_voltage: float

    _actual_mode: str

    _power_supply: PowerSupply

    def __init__(self) -> None:

        self._max_current = 120.0
        self._max_voltage = 80.0
        self._max_power = 3000.0
        self._requested_voltage = 0.0
        self._requested_current = 0.0
        self._requested_power = 0.0

        self._constant_power = False
        self._constant_voltage = True
        self._requested_mode_is_on = False

        self._actual_voltage = 0.0
        self._actual_current = 0.0
        self._actual_power = 0.0

        self._actual_mode = "Unknown"

        self._power_supply = PowerSupply(protocol=UsbProtocol())

        self._load_all_graphics()

    def run(self) -> None:
        self._app_window.after(100, self._update_noise)
        self._app_window.after(100, self._update_actual)
        self._app_window.mainloop()


    def _add_curr_noise_slider_changed(self, event) -> None:
        self._change_add_curr_noise(self._add_curr_noise_slider.get())

    def _add_noise_res_hundredth(self) -> None:
        self._change_slider_resolution(self._add_volt_noise_slider, 0.01)

    def _add_noise_res_tenths(self) -> None:
        self._change_slider_resolution(self._add_volt_noise_slider, 0.1)

    def _add_noise_res_thousandth(self) -> None:
        self._change_slider_resolution(self._add_volt_noise_slider, 0.001)

    def _add_volt_noise_slider_changed(self, event) -> None:
        self._change_add_volt_noise(self._add_volt_noise_slider.get())

    def _center_window(self, window_name: tk.Tk) -> None:
        win_width = window_name.winfo_reqwidth()
        win_height = window_name.winfo_reqheight()
        horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
        vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
        window_name.geometry("+{}+{}".format(horiz_center, vert_center))

    def _change_add_curr_noise(self, add_noise: float) -> None:
        self._add_curr_noise_label.configure(
            text=f"Add Curr Noise: {round(add_noise, 3)}"
        )

    def _change_add_volt_noise(self, add_noise: float) -> None:
        self._add_volt_noise_label.configure(
            text=f"Add Volt Noise: {round(add_noise, 3)}"
        )

    def _change_mult_curr_noise(self, mult_noise: float) -> None:
        self._mult_curr_noise_label.configure(
            text=f"Mult Curr Noise: {round(mult_noise, 3)}"
        )

    def _change_mult_volt_noise(self, mult_noise: float) -> None:
        self._mult_volt_noise_label.configure(
            text=f"{round(mult_noise, 3)}"
        )

    def _change_curr(self, curr: float) -> None:
        if (curr < 0 or curr > self._max_current):
            return
        curr = min(
            curr,
            self._max_power / self._requested_voltage if self._requested_voltage != 0 
            else curr
        )
        self._curr_label.configure(text=f"Current: {round(curr, 3)} A")
        self._power_supply.make_command(Commands.SET_CURR, str(curr))
        self._requested_current = curr
        self._update_power()

    def _change_slider_resolution(self, slider: tk.Scale, res: float) -> None:
        slider.configure(resolution=res)

    def _change_volt(self, volt: float) -> None:
        if (volt < 0 or volt > self._max_voltage):
            return
        volt = min(
            volt,
            self._max_power / self._requested_current if self._requested_current != 0 
            else volt
        )
        self._volt_label.configure(text=f"Voltage: {round(volt, 3)} V")
        self._power_supply.make_command(Commands.SET_VOLTS, str(volt))
        self._requested_voltage = volt
        self._update_power()

    def _click_excel_button(self) -> None:
        # TODO - eventually
        pass

    def _create_additive_noise(self) -> None:
        add_volt_factor = self._add_volt_noise_slider.get()
        self._change_volt(self._requested_voltage + (random() - 0.5)*add_volt_factor)

        add_curr_factor = self._add_curr_noise_slider.get()
        self._change_curr(self._requested_current + (random() - 0.5)*add_curr_factor)

    def _create_frame(self, text: str, row: int, col: int) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(
            self._app_window,
            width = 150,
            text = text
        )
        frame.grid(row=row, column=col, padx=10, pady=10)
        return frame

    def _create_label(self, frame: ttk.LabelFrame, text: str, row: int) -> ttk.Label:
        label = ttk.Label(
            frame,
            text=text
        )
        label.grid(row=row, column=0, padx=10, pady=10)
        return label

    def _create_mult_noise(self) -> None:
        mult_volt_factor = self._mult_volt_noise_slider.get()
        # expect mult_factor to be a number between 0 and 1, most definitely closer to 0 though)
        self._change_volt(
            self._requested_voltage
            * (1 + (random() - 0.5)*mult_volt_factor)
        )

        mult_curr_factor = self._mult_curr_noise_slider.get()
        self._change_curr(
            self._requested_current
            * (1 + (random() - 0.5)*mult_curr_factor)
        )

    def _create_slider(self, frame: ttk.LabelFrame, row: int, max: float, cmd: Callable) -> tk.Scale:
        slider = tk.Scale(
            frame,
            from_=0,
            to=max,
            orient="horizontal",
            resolution=0.001,
            command=cmd
        )
        slider.grid(row=row, column=0, padx=10, pady=10)
        return slider

    def _create_switch(self, frame: ttk.LabelFrame, text: str, cmd: Callable) -> tk.Button:
        button = Button(
            frame,
            text=text,
            width=10,
            command=cmd)
        button.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        return button

    def _curr_slider_changed(self, event) -> None:
        previous_current = self._requested_current
        self._requested_current = self._curr_slider.get()
        if self._requested_current <= previous_current:
            # If we are dropping in current, it is safe.
            # We do this since if voltage is already high and current wants to go high,
            # we should not bump up both values until one of the values is low.
            self._change_curr(self._requested_current)
        if self._constant_power:
            self._requested_voltage = (
                min(self._requested_power / self._requested_current, self._max_voltage) if self._requested_current != 0
                else 0
            )
            self._change_volt(self._requested_voltage)
        if previous_current < self._requested_current:
            self._change_curr(self._requested_current)

    def _curr_res_hundredth(self) -> None:
        self._change_slider_resolution(self._curr_slider, 0.01)

    def _curr_res_int(self) -> None:
        self._change_slider_resolution(self._curr_slider, 1)

    def _curr_res_tenths(self) -> None:
        self._change_slider_resolution(self._curr_slider, 0.1)

    def _curr_res_thousandth(self) -> None:
        self._change_slider_resolution(self._curr_slider, 0.001)

    def _load_all_graphics(self) -> None:
        # Load app window first.
        # Then load frames. Theen load labels since sliders and switches modify it.
        self._load_app_window()
        self._load_frames()
        self._load_labels()

        self._load_sliders()
        self._load_switches()

        self._load_noise_menu()
        self._load_popup_menu()

    def _load_app_window(self) -> None:
        self._app_window = tk.Tk()
        self._app_window.title("Virtual Power Supply")

        self._center_window(self._app_window)

    def _load_frames(self) -> None:
        self._volt_frame = self._create_frame("Requested Voltage", 0, 0)
        self._curr_frame = self._create_frame("Requested Current", 0, 1)
        self._noise_select_frame = self._create_frame("Select Noise Type", 0, 2)
        self._actual_frame = self._create_frame("Actual Values", 0, 3)
        self._add_volt_noise_frame = self._create_frame("Additive Voltage Noise", 1, 0)
        self._add_curr_noise_frame = self._create_frame("Additive Current Noise", 1, 1)
        self._power_frame = self._create_frame("Requested Power", 1, 2)
        self._max_frame = self._create_frame("Change Max Values", 1, 3)
        self._mult_curr_noise_frame = self._create_frame("Multiplicative Current Noise", 2, 1)
        self._mult_volt_noise_frame = self._create_frame("Multiplicative Voltage Noise", 2, 0)
        self._constant_power_frame = self._create_frame("Select Constant/Variable Power", 2, 2)
        self._excel_frame = self._create_frame("Load Excel Data", 2, 3)
        self._on_frame = self._create_frame("Select On/Off", 3, 0)
        self._protocol_frame = self._create_frame("Select Protocol", 3, 1)
        self._volt_curr_constant_frame = self._create_frame("Keep Voltage/Current Constant", 3, 2)

    def _load_labels(self) -> None:
        self._actual_current_label = self._create_label(self._actual_frame, "Current: 0.0 A", 1)
        self._actual_mode_label = self._create_label(self._actual_frame, "Mode: Unknown", 3)
        self._actual_power_label = self._create_label(self._actual_frame, "Power: 0.0 W", 2)
        self._actual_voltage_label = self._create_label(self._actual_frame, "Voltage: 0.0 V", 0)
        self._add_curr_noise_label = self._create_label(self._add_curr_noise_frame, "Add Curr Noise: 0.0", 0)
        self._add_volt_noise_label = self._create_label(self._add_volt_noise_frame, "Add Volt Noise: 0.0", 0)
        self._constant_power_label = self._create_label(self._constant_power_frame, "Currently using variable power", 0)
        self._curr_label = self._create_label(self._curr_frame, "Curent: 0.0 A", 0)
        self._mult_curr_noise_label = self._create_label(self._mult_curr_noise_frame, "Mult Curr Noise: 0.0", 0)
        self._mult_volt_noise_label = self._create_label(self._mult_volt_noise_frame, "Mult Volt Noise: 0.0", 0)
        self._on_label = self._create_label(self._on_frame, "Currently off", 0)
        self._power_label = self._create_label(self._power_frame, "Power: 0.0 W", 0)
        self._protocol_label = self._create_label(self._protocol_frame, "Currently using USB", 0)
        self._volt_curr_constant_label = self._create_label(self._volt_curr_constant_frame, "Currently using constant voltage", 0)
        self._volt_label = self._create_label(self._volt_frame, "Voltage: 0.0 V", 0)

    def _load_noise_menu(self) -> None:
        choices = ["None", "Additive", "Multiplicative"]
        self._noise_status = tk.StringVar()
        self._noise_status.set(choices[0])
        self._noise_menu = tk.OptionMenu(self._noise_select_frame, self._noise_status, *choices)
        self._noise_menu.grid(row=0, column=0, padx=10, pady=10)

    def _load_popup_menu(self) -> None:
        self._popup_menu = tk.Menu(self._app_window, tearoff=False)
        self._popup_menu.add_command(
            label="Change voltage slider resolution to 1",
            command=self._volt_res_int)
        self._popup_menu.add_command(
            label="Change voltage slider resolution to 0.1",
            command=self._volt_res_tenths)
        self._popup_menu.add_command(
            label="Change voltage slider resolution to 0.01",
            command=self._volt_res_hundredth)
        self._popup_menu.add_command(
            label="Change voltage slider resolution to 0.001",
            command=self._volt_res_thousandth)
        self._popup_menu.add_separator()
        self._popup_menu.add_command(
            label="Change current slider resolution to 1",
            command=self._curr_res_int)
        self._popup_menu.add_command(
            label="Change current slider resolution to 0.1",
            command=self._curr_res_tenths)
        self._popup_menu.add_command(
            label="Change current slider resolution to 0.01",
            command=self._curr_res_hundredth)
        self._popup_menu.add_command(
            label="Change current slider resolution to 0.001",
            command=self._curr_res_thousandth)
        self._popup_menu.add_separator()
        self._popup_menu.add_command(
            label="Change add noise slider resolution to 0.1",
            command=self._add_noise_res_tenths)
        self._popup_menu.add_command(
            label="Change add noise slider resolution to 0.01",
            command=self._add_noise_res_hundredth)
        self._popup_menu.add_command(
            label="Change add noise slider resolution to 0.001",
            command=self._add_noise_res_thousandth)
        self._popup_menu.add_separator()
        self._popup_menu.add_command(
            label="Change mult noise slider resolution to 0.1",
            command=self._mult_noise_res_tenths)
        self._popup_menu.add_command(
            label="Change mult noise slider resolution to 0.01",
            command=self._mult_noise_res_hundredth)
        self._popup_menu.add_command(
            label="Change mult noise slider resolution to 0.001",
            command=self._mult_noise_res_thousandth)
        
        self._app_window.bind("<Button-3>", self._show_popup_menu)

    def _load_sliders(self) -> None:
        self._add_curr_noise_slider = self._create_slider(self._add_curr_noise_frame, 1, 1, self._add_curr_noise_slider_changed)
        self._add_volt_noise_slider = self._create_slider(self._add_volt_noise_frame, 1, 1, self._add_volt_noise_slider_changed)
        self._curr_slider = self._create_slider(self._curr_frame, 1, self._max_current, self._curr_slider_changed)
        self._max_curr_slider = self._create_slider(self._max_frame, 1, 120, self._max_curr_slider_changed)
        self._max_power_slider = self._create_slider(self._max_frame, 3, 3000, self._max_power_slider_changed)
        self._max_volt_slider = self._create_slider(self._max_frame, 2, 80, self._max_volt_slider_changed)
        self._mult_curr_noise_slider = self._create_slider(self._mult_curr_noise_frame, 1, 0.4, self._mult_curr_noise_slider_changed)
        self._mult_volt_noise_slider = self._create_slider(self._mult_volt_noise_frame, 1, 0.4, self._mult_volt_noise_slider_changed)
        self._power_slider = self._create_slider(self._power_frame, 1, self._max_power, self._power_slider_changed)
        self._volt_slider = self._create_slider(self._volt_frame, 1, self._max_voltage, self._volt_slider_changed)

    def _load_switches(self) -> None:
        self._constant_power_button = self._create_switch(self._constant_power_frame, "Change to constant power", self._toggle_constant_power_switch)
        self._excel_button = self._create_switch(self._excel_frame, "Load excel data", self._click_excel_button)
        self._on_button = self._create_switch(self._on_frame, "Turn on", self._toggle_on_switch)
        self._protocol_button = self._create_switch(self._protocol_frame, "Change to Ethernet", self._toggle_protocol_switch)
        self._volt_curr_constant_button = self._create_switch(self._volt_curr_constant_frame, "Change to constant current", self._toggle_volt_curr_constant_switch)

    def _max_curr_slider_changed(self, event) -> None:
        self._max_current = self._max_curr_slider.get()
        self._curr_slider = self._create_slider(self._curr_frame, 1, self._max_current, self._curr_slider_changed)

    def _max_power_slider_changed(self, event) -> None:
        self._max_power = self._max_power_slider.get()
        self._power_slider = self._create_slider(self._power_frame, 1, self._max_power, self._power_slider_changed)

    def _max_volt_slider_changed(self, event) -> None:
        self._max_voltage = self._max_volt_slider.get()
        self._volt_slider = self._create_slider(self._volt_frame, 1, self._max_voltage, self._volt_slider_changed)

    def _mult_curr_noise_slider_changed(self, event) -> None:
        self._change_mult_curr_noise(self._mult_curr_noise_slider.get())        

    def _mult_noise_res_hundredth(self) -> None:
        self._change_slider_resolution(self._mult_volt_noise_slider, 0.01)

    def _mult_noise_res_tenths(self) -> None:
        self._change_slider_resolution(self._mult_volt_noise_slider, 0.1)

    def _mult_noise_res_thousandth(self) -> None:
        self._change_slider_resolution(self._mult_volt_noise_slider, 0.001)

    def _mult_volt_noise_slider_changed(self, event) -> None:
        self._change_mult_volt_noise(self._mult_volt_noise_slider.get())

    def _power_slider_changed(self, event) -> None:
        self._requested_power = self._power_slider.get()
        if not self._constant_power:
            return
        if self._constant_voltage:
            self._requested_current = (
                min(self._requested_power / self._requested_voltage, self._max_current) if self._requested_voltage != 0
                else 0
            )
            self._change_curr(self._requested_current)
        if not self._constant_voltage:
            self._requested_voltage = (
                min(self._requested_power / self._requested_current, self._max_voltage) if self._requested_current != 0
                else 0
            )
            self._change_volt(self._requested_voltage)

    def _show_popup_menu(self, event) -> None:
        self._popup_menu.tk_popup(event.x_root, event.y_root)

    def _toggle_constant_power_switch(self) -> None:
        if self._constant_power_button.config("text")[-1] == "Change to constant power":
            self._constant_power = True
            self._constant_power_label.configure(text="Currently using constant power")
            self._constant_power_button.config(text="Change to variable power")
        else:
            self._constant_power = False
            self._constant_power_label.config(text="Currently using variable power")
            self._constant_power_button.config(text="Change to constant power")

    def _toggle_on_switch(self) -> None:
        if self._on_button.config("text")[-1] == "Turn on":
            self._requested_mode_is_on = True
            self._on_label.configure(text=f"Currently on")
            self._on_button.config(text="Turn off")
            self._power_supply.make_command(Commands.SET_CHANNEL_STATE, str(0))
        else:
            self._requested_mode_is_on = False
            self._on_label.configure(text=f"Currently off")
            self._on_button.config(text="Turn on")
            self._power_supply.make_command(Commands.SET_CHANNEL_STATE, str(1))

    def _toggle_protocol_switch(self) -> None:
        # TODO - need to change this eventually to be EthernetProtocol and UsbProtocol
        if self._protocol_button.config("text")[-1] == "Change to USB":
            self._protocol_label.configure(text="Currently using USB")
            self._protocol_button.config(text="Change to Ethernet")
            self._power_supply = PowerSupply(protocol=UsbProtocol())
        else:
            self._protocol_label.config(text="Currently using Ethernet")
            self._protocol_button.config(text="Change to USB")
            self._power_supply = PowerSupply(protocol=EthernetProtocol())

    def _toggle_volt_curr_constant_switch(self) -> None:
        if self._volt_curr_constant_button.config("text")[-1] == "Change to constant current":
            self._constant_voltage = False
            self._volt_curr_constant_label.configure(text="Currently using constant current")
            self._volt_curr_constant_button.config(text="Change to constant voltage")
        else:
            self._constant_voltage = True
            self._volt_curr_constant_label.config(text="Currently using constant voltage")
            self._volt_curr_constant_button.config(text="Change to constant current")

    def _update_actual(self) -> None:
        try:
            self._actual_voltage = float(self._power_supply.make_command(Commands.GET_VOLTS))
        except ValueError:
            # falls here since make_command for debugging is not real
            self._actual_voltage = round(random() * -1, 3)  # done for debugging purposes
        self._actual_voltage_label.configure(text=f"Voltage: {round(self._actual_voltage, 3)} V")
        try:
            self._actual_current = float(self._power_supply.make_command(Commands.GET_CURR))
        except ValueError:
            # falls here since make_command for debugging is not real
            self._actual_current = round(random() * -1, 3)  # done for debugging purposes
        self._actual_current_label.configure(text=f"Current: {round(self._actual_current, 3)} A")
        try:
            self._actual_power = self._actual_voltage * self._actual_current
        except ValueError:
            # should no longer enter here
            self._actual_power = 0
        self._actual_power_label.configure(text=f"Power: {round(self._actual_power, 3)} W")
        self._actual_mode = self._power_supply.make_command(Commands.GET_OUT_MODE)
        self._actual_mode_label.configure(text=f"Mode: {self._actual_mode}")
        self._app_window.after(100, self._update_actual)

    def _update_noise(self) -> None:
        if not self._requested_mode_is_on:
            pass
        elif self._noise_status.get() == "None":
            pass
        elif self._noise_status.get() == "Additive":
            self._create_additive_noise()
        elif self._noise_status.get() == "Multiplicative":
            self._create_mult_noise()
        self._app_window.after(100, self._update_noise)
    
    def _update_power(self) -> None:
        self._power_label.configure(
            text=f"Power: {round(self._requested_voltage * self._requested_current, 3)} W"
        )

    def _volt_res_hundredth(self) -> None:
        self._change_slider_resolution(self._volt_slider, 0.01)

    def _volt_res_int(self) -> None:
        self._change_slider_resolution(self._volt_slider, 1)

    def _volt_res_tenths(self) -> None:
        self._change_slider_resolution(self._volt_slider, 0.1)

    def _volt_res_thousandth(self) -> None:
        self._change_slider_resolution(self._volt_slider, 0.001)

    def _volt_slider_changed(self, event) -> None:
        previous_voltage = self._requested_voltage
        self._requested_voltage = self._volt_slider.get()
        if self._requested_voltage <= previous_voltage:
            # If we are dropping in voltage, it is safe.
            # We do this since if current is already high and voltage wants to go high,
            # we should not bump up both values until one of the values is low.
            self._change_volt(self._requested_voltage)
        if self._constant_power:
            self._requested_current = (
                min(self._requested_power / self._requested_voltage, self._max_current) if self._requested_voltage != 0
                else 0
            )
            self._change_curr(self._requested_current)
        if previous_voltage < self._requested_voltage:
            self._change_volt(self._requested_voltage)


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()