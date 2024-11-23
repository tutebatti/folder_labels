import configparser


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
