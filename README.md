# Controlling Power Supply via Python

power_supply.py is currently a WIP and draft for controlling the Elektro-Automatik Power Supply using Python.

## Power Supply Info

We are using the [Elektro-Automatik EA-PS 9080-120 Power Supply](https://www.tequipment.net/Elektro-Automatik/EA-PS-9080-120-2U/DC-Power-Supplies/Lab-Power-Supplies/#docs)

Capable of up to 3000W, 80V, 120A.

## How to Control

Use the SCPI command set by referring to the [PSU SCPI reference manual](https://www.envox.eu/bench-power-supply/psu-scpi-reference-manual/psu-scpi-commands-summary/).

There are many [examples](https://www.envox.eu/bench-power-supply/psu-scpi-reference-manual/psu-scpi-programming-examples/) online.

The communication protocol for the Elektro Automatik should be either Ethernet or USB. There are many examples of how to communicate using these protocols [online](https://magna-power.com/learn/kb/instrumentation-programming-with-python) using SCPI.

Check external documentation such as the Elektro Automatik reference manual, datasheet, and "Programming Guide ModBus and SCPI" document.

## Tests

No tests have been done yet

## Program

graphic_display.py is to act as a virtual power supply.
Can run 
`python3 set_voltage.py [insert_voltage_in_volts]`
or
`python3 set_voltage.py [insert_current_in_amps]`,
which assumes USB connection.

To open the graphic_display, run
`python3 graphic_display.py`
or double click the executable.

To generate a new executable after creating new code, 
run
`python3 -m PyInstaller --onefile --windowed graphic_display.py`
and then locate graphic_display.exe in the dist folder.

# TODO 

- [ ] Ethernet and USB protocols have not been tested
- [ ] Excel sheet button has not been fully developed
- [ ] Actual values section is currently faked