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
        config = Config()

        config.styles = Styles.from_ini(ini_file)

        config.measures = Measures.from_ini(ini_file)
        config.measures.calculate_symbol_width(config.styles)

        config.widths = widths_from_ini(ini_file)
        config.letters = letters_from_ini(ini_file)

        return config

config_file = 'config_example.ini'
config = Config.from_ini(config_file)
