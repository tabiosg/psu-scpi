import sys

from power_supply import Commands, DebugProtocol, PowerSupply


def main():
    power_supply = PowerSupply(protocol=DebugProtocol())
    power_supply.make_command(Commands.SET_VOLTS, sys.argv[1])

if __name__ == "__main__":
    main()