from configparser import ConfigParser

from src.config.util import validate_config_section, validate_string


class Letters:
    config_parser = ConfigParser
    dictionary: dict[str, str]

    @classmethod
    def from_ini(cls, ini_file: str) -> dict:
        letters = Letters()
        letters.config_parser = ConfigParser()
        letters.config_parser.optionxform = str
        letters.config_parser.read(ini_file)

        validate_config_section("Letters", letters.config_parser)

        return letters.dictionary

    @property
    def dictionary(self):
        letter_dict: dict[str, str] = dict()
        for k, v in self.config_parser["Letters"].items():
            validate_string(k)
            validate_string(v)
            letter_dict[k] = v.strip('"').strip()
        return letter_dict
