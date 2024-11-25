from configparser import ConfigParser

from reportlab.lib.units import cm

from src.config.util import validate_config_section, validate_string


class Widths:
    config_parser = ConfigParser
    dictionary: dict[str, float]

    @classmethod
    def from_ini(cls, ini_file: str) -> dict:
        widths = Widths()
        widths.config_parser = ConfigParser()
        widths.config_parser.read(ini_file)
        validate_config_section("Widths", widths.config_parser)

        return widths.dictionary

    @property
    def dictionary(self):
        width_dict: dict[str, float] = dict()

        for k, v in self.config_parser["Widths"].items():
            validate_string(k)
            try:
                value = float(v)
            except ValueError:
                raise ValueError(f"Invalid float value: {v}")

            width_dict[k] = value * cm

        return width_dict
