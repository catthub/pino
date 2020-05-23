from typing import Dict, List, Optional

import yaml
from serial.tools import list_ports


class Config(dict):
    def __init__(self, path: str) -> None:
        f = open(path, "r")
        self.__path = path
        d: dict = yaml.safe_load(f)
        [self.__setitem__(item[0], item[1]) for item in d.items()]
        f.close()

    def __missing__(self) -> dict:
        return dict()

    def get_comport(self) -> dict:
        return self["Comport"]

    def get_experimental(self) -> Optional[dict]:
        return self["Experimental"]

    def get_metadata(self) -> Optional[dict]:
        self["Metadata"]


Info = Dict[str, Dict[str, str]]


class PortAPI(object):
    def __init__(self):
        self.__ports = list_ports.comports()

    def reload(self):
        self.__ports = list_ports.comports()

    def get_device(self) -> List[str]:
        return [port.device for port in self.__ports]

    def get_serial_number(self) -> List[str]:
        return [port.serial_number for port in self.__ports]

    def get_manufacture(self) -> List[str]:
        return [port.manufacturer for port in self.__ports]

    def get_name(self) -> List[str]:
        return [port.name for port in self.__ports]

    def get_location(self) -> List[str]:
        return [port.location for port in self.__ports]

    def get_info(self) -> Info:
        ret: Info = {}
        for port in self.__ports:
            dev = port.device
            name = port.name
            serial = port.serial_number
            loc = port.location
            man = port.manufacturer
            ret[dev] = {
                "name": name,
                "serial-number": serial,
                "location": loc,
                "manufacturer": man
            }
        return ret
