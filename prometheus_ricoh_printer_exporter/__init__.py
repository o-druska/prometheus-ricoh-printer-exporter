from os.path import join as opj
from pathlib import Path


class Configuration:
    def __init__(self):
        self._home = str(Path.home())
        self._weather_exporter_dir = opj(self._home, '.prometheus_ricoh_printer_exporter')


__params__ = Configuration()
__all__ = ['__version__', '__params__']