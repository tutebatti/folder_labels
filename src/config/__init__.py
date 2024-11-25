from typing import Dict

from src.config.measures import Measures
from src.config.styles import Styles
from src.config.util import letters_from_ini, widths_from_ini


class Config:
    styles: Styles
    measures: Measures
    widths: Dict[str, float]
    letters: Dict[str, str]

    @classmethod
    def from_ini(cls, ini_file: str):
        cfg = Config()

        cfg.styles = Styles.from_ini(ini_file)

        cfg.measures = Measures.from_ini(ini_file)
        cfg.measures.calculate_symbol_width(cfg.styles)

        cfg.widths = widths_from_ini(ini_file)
        cfg.letters = letters_from_ini(ini_file)

        return cfg


config_file = 'config_example.ini'
config = Config.from_ini(config_file)
