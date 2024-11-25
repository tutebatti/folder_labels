import configparser
from configparser import ConfigParser

from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics


def determine_scale_factor(string: str, fontsize: int, max_width: float) -> float:
    from src.config import config
    string_width: float = pdfmetrics.stringWidth(string, config.styles.font, fontsize)
    return max_width / string_width * 0.9 if string_width >= max_width else 1


def letters_from_ini(ini_file: str) -> dict:
    config_parser = ConfigParser()
    config_parser.optionxform = str
    config_parser.read(ini_file)

    validate_config_section("Letters", config_parser)

    return letter_dict_from_config_parser(config_parser)


def letter_dict_from_config_parser(config_parser: ConfigParser):
    letter_dict: dict[str, str] = dict()
    for k, v in config_parser["Letters"].items():
        validate_string(k)
        validate_string(v)
        letter_dict[k] = v.strip('"').strip()
    return letter_dict


def widths_from_ini(ini_file: str) -> dict:
    config_parser = ConfigParser()
    config_parser.read(ini_file)
    validate_config_section("Widths", config_parser)
    return width_dict_from_config_parser(config_parser)


def width_dict_from_config_parser(config_parser: ConfigParser):
    width_dict: dict[str, float] = dict()

    for k, v in config_parser["Widths"].items():
        validate_string(k)
        try:
            value = float(v)
        except ValueError:
            raise ValueError(f"Invalid float value: {v}")

        width_dict[k] = value * cm

    return width_dict


def validate_string(k: str):
    if not isinstance(k, str):
        raise ValueError(f"Invalid name value (must be a string): {k}")


def validate_config_section(section: str, config_parser: ConfigParser):
    check_for_missing_section(section, config_parser)
    check_for_duplicates(section, config_parser)


def check_for_missing_section(section: str, config_parser: ConfigParser):
    if section not in config_parser:
        raise ValueError(f"Section {section} missing in config")


def check_for_duplicates(section: str, config_parser: ConfigParser):
    values = set()
    for k, v in config_parser[section].items():
        if v in values:
            raise ValueError(f"{k} has the duplicate value {v} compared to another key")
        else:
            values.add(v)


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


def get_float(config_parser: configparser.ConfigParser, section: str, option: str) -> float:
    """Helper method to safely convert an INI value to a float"""
    value = config_parser[section].get(option)
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid float value for \"{option}\" in section \"{section}\": {value}")
