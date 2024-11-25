from src.config.measures import Measures
from src.config.styles import Styles
from src.config.widths import Widths
from src.config.letters import Letters


class Config:
    styles: Styles
    measures: Measures
    widths: dict[str, float]
    letters: dict[str, str]

    @classmethod
    def from_ini(cls, ini_file: str):
        config = Config()

        config.styles = Styles.from_ini(ini_file)

        config.measures = Measures.from_ini(ini_file)
        config.measures.calculate_symbol_width(config.styles)

        config.widths = Widths.from_ini(ini_file)
        config.letters = Letters.from_ini(ini_file)

        return config
