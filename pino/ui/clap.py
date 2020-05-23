import argparse as ap
import os.path
from importlib.util import module_from_spec, spec_from_file_location

from pino.config import Config


class PinoCli(object):
    def __init__(self):
        self.__parser = ap.ArgumentParser(description="About this program")
        self.__parser.add_argument("--yaml", "-y", help="About This argument")
        self.__parser.add_argument("--filename",
                                   "-f",
                                   help="About This argument")
        self.__args = self.__parser.parse_args()
        self.__main = []

    def get_config(self) -> Config:
        yml = self.__args.yaml
        return Config(yml)

    def get_filename(self) -> str:
        return self.__args.filename

    def load_main(self, f: str):
        name = os.path.splitext(os.path.basename(f))[0]
        spec = spec_from_file_location(name, f)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.__main.append(mod.__getattribute__("main"))

    def run_main(self):
        [m() for m in self.__main]
