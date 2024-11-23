import configparser
from enum import Enum
from typing import Type, Dict

from src.config.measures import Measures


class Width(Enum):

    @classmethod
    def from_ini(cls, ini_file: str) -> Type[Enum]:
        config_parser = configparser.ConfigParser()
        config_parser.read(ini_file)

        width_dict: Dict[str, float] = dict()
        for k, v in config_parser["Widths"].items():
            try:
                value = float(v)
            except ValueError:
                raise ValueError(f"Invalid float value for \"{k}\" in section \"Widths\": {v}")
            width_dict[k] = value * Measures.CM_TO_POINTS

        for k, v in width_dict.items():
            if v in cls._value2member_map_:
                raise ValueError(f"Duplicate value found: {v} for {k}")
            setattr(cls, k, v)

        return cls
