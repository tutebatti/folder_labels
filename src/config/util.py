import configparser
from configparser import ConfigParser

from reportlab.pdfbase import pdfmetrics


def determine_scale_factor(string: str, fontsize: int, max_width: float) -> float:
    from src.config import config
    string_width: float = pdfmetrics.stringWidth(string, config.styles.font, fontsize)
    return max_width / string_width * 0.9 if string_width >= max_width else 1


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
