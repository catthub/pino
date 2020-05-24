import os
import sys
from enum import Enum
from subprocess import call, check_output
from time import sleep
from typing import Dict, Optional

from serial import Serial, SerialException  # type: ignore


class Comport(object):
    def __init__(self):
        if sys.platform == "win32":
            self.__arduino = os.path.join(os.environ["ProgramFiles(x86)"],
                                          "Arduino", "arduino_debug.exe")
        else:
            self.__arduino = "arduino"
        self.__port = ""
        self.__timeout = None
        self.__baudrate = 115200
        self.__dotino = ""
        self.__warmup: Optional[float] = None

    def __del__(self):
        self.__conn.reset_input_buffer()
        self.__conn.reset_output_buffer()
        self.disconnect()

    def apply_settings(self, settings: Dict) -> 'Comport':
        available_settings = [
            "arduino", "port", "baudrate", "timeout", "dotino", "warmup"
        ]
        for k in available_settings:
            if k == "arduino":
                val = settings.get(k)
                if val is not None:
                    self.set_arduino(val)
            if k == "port":
                val = settings.get(k)
                if val is not None:
                    self.set_port(val)
            if k == "baudrate":
                val = settings.get(k)
                if val is not None:
                    self.set_baudrate(val)
            if k == "timeout":
                val = settings.get(k)
                if val is not None:
                    self.set_timeout(val)
            if k == "dotino":
                val = settings.get(k)
                if val is not None:
                    self.set_inofile(val)
            if k == "warmup":
                val = settings.get(k)
                if val is not None:
                    self.set_warmup(val)
        return self

    def set_arduino(self, arduino: str) -> 'Comport':
        self.__arduino = arduino
        return self

    def set_port(self, port: str) -> 'Comport':
        self.__port = port
        return self

    def set_baudrate(self, baudrate: int) -> 'Comport':
        if baudrate not in Serial.BAUDRATES:
            raise SerialException("Given baudrate cannot be used")
        self.__baudrate = baudrate
        return self

    def set_timeout(self, timeout: Optional[float]) -> 'Comport':
        self.__timeout = timeout
        return self

    def set_inofile(self, path: str) -> 'Comport':
        self.__dotino = path
        return self

    def set_warmup(self, duration: float) -> 'Comport':
        self.__warmup = duration
        return self

    def connect(self) -> 'Comport':
        self.__conn = Serial(self.__port,
                             self.__baudrate,
                             timeout=self.__timeout)
        if self.__warmup is not None:
            t: float = self.__warmup
            sleep(t)
        return self

    def disconnect(self):
        """disconnect serial port"""
        try:
            self.__conn.close()
        except SerialException:
            pass
        return None

    @staticmethod
    def __as_command(binary: str, upload: str, port: str) -> str:
        return f"{binary} --upload {upload}, --port {port}"

    def deploy(self) -> 'Comport':
        """Write arduino program to connected board"""
        if self.__port == "":
            raise SerialException("Port must be specified")
#        if sys.platform == "win32":
#            call(self.__as_command(self.__arduino, self.__dotino, self.__port),
#                 shell=True)
#            return None
        check_output(self.__as_command(self.__arduino, self.__dotino,
                                       self.__port),
                     shell=True)
        return self

    def get_connection(self) -> Serial:
        return self.__conn


def as_bytes(x: int) -> bytes:
    return x.to_bytes(1, "little")


class PinMode(Enum):
    INPUT = 0
    INPUT_PULLUP = 1
    OUTPUT = 2
    SERVO = 3


INPUT = PinMode.INPUT
INPUT_PULLUP = PinMode.INPUT_PULLUP
OUTPUT = PinMode.OUTPUT


class PinState(Enum):
    LOW = 0
    HIGH = 1


LOW = PinState.LOW
HIGH = PinState.HIGH


class Arduino(object):
    def __init__(self, comport: Comport):
        self.__conn = comport.get_connection()

    def set_pinmode(self, pin: int, mode: PinMode) -> None:
        proto = b'\x00' + as_bytes(pin + 12 * mode.value)
        self.__conn.write(proto)

    def digital_write(self, pin: int, state: PinState) -> None:
        proto = b'\x01' + as_bytes(pin + 12 * state.value)
        self.__conn.write(proto)

    def digital_read(self, pin, size=0, timeout=None) -> bytes:
        proto = b'\x02' + as_bytes(pin)
        self.__conn.write(proto, timeout)
        return self.__conn.read(size)

    def analog_write(self, pin: int, v: int) -> None:
        proto = b'\x01' + as_bytes(pin + 12 * 2) + as_bytes(v)
        self.__conn.write(proto)

    def analog_read(self, pin, size=0, timeout=None) -> bytes:
        proto = b'\x02' + as_bytes(pin + 12)
        self.__conn.write(proto, timeout)
        return self.__conn.read(size)

    def read_until_eol(self) -> str:
        return self.__conn.readline()

    def disconnect(self):
        self.__conn.reset_input_buffer()
        self.__conn.reset_output_buffer()
        self.__conn.close()

    def servo_rotate(self, pin: int, angle: int) -> None:
        proto = b'\x01' + as_bytes(pin + 12 * 3) + as_bytes(angle)
        self.__conn.write(proto)
