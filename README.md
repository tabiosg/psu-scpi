# Controlling Power Supply via Python/Matlab

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

Assigned July 21, 2022

## Program

graphic_display.py is to act as a virtual power supply.

## todo

set example of how to change voltage

set_Voltage.py 50V
increments -> min and max

Read a spreadsheet from excel

add a button to put fluctuation to current
white noise: current + noise
or multiplicative noise: current * noise
wxPython for graphics

lex and yacc are interesting

What happens if voltage and power exceed power? Should we prevent this from happening in the first place?

When adding noise, do you change voltage? current? both?

for code, make it alphabetical