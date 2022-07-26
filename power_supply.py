import socket
from enum import Enum

import serial


class CmdType(Enum):
    GET = 0
    SET = 1


class ScpiCommand(object):

    command: str
    type: CmdType

    def __init__(self, cmd: str = "") -> None:
        pass


class GetCmd(ScpiCommand):
    command: str
    type: CmdType

    def __init__(self, cmd: str = "") -> None:
        self.command = cmd
        self.type = CmdType.GET


class SetCmd(ScpiCommand):
    command: str
    type: CmdType

    def __init__(self, cmd: str = "") -> None:
        self.command = cmd
        self.type = CmdType.SET


class Commands():
    # TODO - Add more commands as desired
    GET_VOLTS = GetCmd("MEAS:VOLT?")
    # TODO - For something like SET_VOLTS, maybe check that
    # arguments are between U-min=10V and U-max=75V
    # (otherwise, it will error according to the reference manual)
    # SIMILARLY, I-min is 5.0A and  I-max is 100.0A.
    SET_VOLTS = SetCmd("VOLT")
    GET_CURR = GetCmd("MEAS:CURR?")
    SET_CURR = SetCmd("CURR")
    GET_OCP_STATE = GetCmd("CURR:PROT:STAT?")
    SET_OCP_STATE = SetCmd("CURR:PROT:STAT")
    SET_OCP_DELAY = SetCmd("CURR:PROT:DEL")
    GET_OUT_CHANNEL = GetCmd("INST?")
    SET_OUT_CHANNEL = SetCmd("INST CH")
    GET_OUT_MODE = GetCmd("OUTP:MODE?")
    SET_CHANNEL_STATE = SetCmd("OUTP")
    RESET = SetCmd("*RST")
    GET_ID_STRING = GetCmd("*IDN?")
    EXEC_SELF_TEST_AND_GET_RESULT = GetCmd("*TST?")
    GET_MORE_SELF_TEST_INFO = GetCmd("DIAG:TEST?")
    CLEAR = SetCmd("*CLS")
    GET_EVENT_STATUS_REG = GetCmd("*ESR?")


class Protocol(object):
    
    def __init__(self) -> None:
        pass


class UsbProtocol(Protocol):

    # TODO - Verify that ports and baudrate are accurate
    def __init__(self, port: str = "COM8", baudrate: int = 115200) -> None:
        try:
            self.conn = serial.Serial(port=port, baudrate=baudrate)
        except:
            pass

    def write(self, msg: str = "") -> None:
        # TODO - Test that USB write works
        try:
            self.conn.write(msg)
        except:
            pass

    def read(self) -> str:
        # TODO - Test that USB read works
        response = ""
        try:
            response = self.conn.readline()
        except:
            pass
        return response

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass


class EthernetProtocol(Protocol):

    # TODO - Verify that IP is accurate (192.168.0.2 is usually the default ip)
    # According to the reference manual, the standard port is 5025
    def __init__(self, ip: str = "192.168.0.2", port: int = 5025) -> None:
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # TODO - COMMENTED OUT TEMPORARILY BECAUSE PROGRAM GETS STUCK ON THIS
            # self.s.connect((ip, port))
        except:
            pass

    def write(self, msg: str = "") -> None:
        # TODO - Test that Ethernet write works
        try:
            self.s.sendall(msg)
        except:
            pass

    def read(self) -> str:
        # TODO - Test that Ethernet read works
        response = ""
        try:
            response = self.s.recv()
        except:
            pass
        return response

    def __del__(self):
        try:
            self.s.close()
        except:
            pass

class DebugProtocol(Protocol):

    def __init__(self) -> None:
        pass

    def write(self, msg: str = "") -> None:
        print(msg)

    def read(self) -> str:
        return "READ DEBUG\n"


class PowerSupply:
    
    def __init__(self, protocol: Protocol = UsbProtocol) -> None:
        self.protocol = protocol

    def make_command(self, scpi_command: ScpiCommand, arg_0: str = "", arg_1: str = "") -> str:
        self.protocol.write(f"{scpi_command.command} {arg_0} {arg_1}\n")
        if scpi_command.type == CmdType.SET:
            return ""
        return self.protocol.read()


def example_usage_one():
    """Sets the voltage and gets the voltage of the power supply"""
    print("EXAMPLE USE ONE \n")
    power_supply = PowerSupply(protocol=DebugProtocol())
    power_supply.make_command(Commands.RESET)
    print(power_supply.make_command(Commands.GET_OUT_CHANNEL))
    # TODO - Verify available channels on our Power Supply
    power_supply.make_command(Commands.SET_OUT_CHANNEL, "CH1")
    print(power_supply.make_command(Commands.GET_VOLTS))
    power_supply.make_command(Commands.SET_VOLTS, 10.0)
    print(power_supply.make_command(Commands.GET_VOLTS))
    power_supply.make_command(Commands.SET_OCP_STATE, 1)
    power_supply.make_command(Commands.SET_OCP_DELAY, "100ms")
    print(power_supply.make_command(Commands.GET_CURR))

def example_usage_two():
    """Gets identification info and self-test results"""
    print("EXAMPLE USE TWO \n")
    power_supply = PowerSupply(protocol=DebugProtocol())
    power_supply.make_command(Commands.RESET)
    power_supply.make_command(Commands.SET_OUT_CHANNEL, "CH1")
    power_supply.make_command(Commands.GET_ID_STRING)
    power_supply.make_command(Commands.EXEC_SELF_TEST_AND_GET_RESULT)
    power_supply.make_command(Commands.GET_MORE_SELF_TEST_INFO)

def example_turn_off():
    """Turns off the power supply output"""
    power_supply = PowerSupply(protocol=DebugProtocol())
    power_supply.make_command(Commands.SET_OUT_CHANNEL, "CH1")
    power_supply.make_command(Commands.SET_OCP_STATE, "OFF")
    

def main():
    example_usage_one()
    example_usage_two()

if __name__ == "__main__":
    main()