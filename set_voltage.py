import sys

from power_supply import Commands, DebugProtocol, EthernetProtcol, PowerSupply, UsbProtocol


def main():
    power_supply = PowerSupply(protocol=UsbProtocol())
    power_supply.make_command(Commands.SET_VOLTS, sys.argv[1])

if __name__ == "__main__":
    main()