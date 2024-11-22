import configparser
from configparser import ConfigParser
from typing import Dict

from reportlab.pdfbase import pdfmetrics

CM_TO_POINTS: float = 28.35 # leave unchanged

def str_to_bool(value: str) -> bool:
    """Helper method to convert string to boolean"""
    if value.lower() in ["true", "1", "yes"]:
        return True
    elif value.lower() in ["false", "0", "no"]:
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")


def get_int(config_parser: configparser.ConfigParser, section: str, option: str) -> int:
    """Helper method to safely convert an INI value to an integer"""
    value = config_parser[section].get(option)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid integer value for \"{option}\" in section \"{section}\": {value}")


def determine_scale_factor(string: str, fontsize: int, max_width: float) -> float:
    from src.config import config
    string_width: float = pdfmetrics.stringWidth(string, config.styles.font, fontsize)
    return max_width / string_width * 0.9 if string_width >= max_width else 1


def letters_from_ini(ini_file: str) -> dict:
    config_parser = ConfigParser()
    config_parser.optionxform = str
    config_parser.read(ini_file)

    letter_dict: Dict[str, str] = dict()
    for k, v in config_parser["Letters"].items():
        if not isinstance(k, str):
            raise ValueError(f"Invalid name value (must be a string): {k}")
        if not isinstance(v, str):
            raise ValueError(f"Invalid string value: {v}")
        letter_dict[k] = v.strip('"').strip()

    # TODO: check for duplicate values

    return letter_dict

def widths_from_ini(ini_file: str) -> dict:
    config_parser = ConfigParser()
    config_parser.read(ini_file)

    width_dict: Dict[str, float] = dict()
    for k, v in config_parser["Widths"].items():
        if not isinstance(k, str):
            raise ValueError(f"Invalid name value (must be a string): {k}")
        try:
            value = float(v)
        except ValueError:
            raise ValueError(f"Invalid float value: {v}")
        width_dict[k] = value * CM_TO_POINTS

    # TODO: check for duplicate values

    return width_dict
