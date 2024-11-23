import configparser
from enum import Enum
from typing import Type, Dict


class Letter(Enum):

    @classmethod
    def from_ini(cls, ini_file: str) -> Type[Enum]:
        config_parser = configparser.ConfigParser()
        config_parser.read(ini_file)

        letter_dict: Dict[str, str] = {}
        for k, v in config_parser["Letters"].items():
            if not isinstance(k, str):
                raise ValueError(f"Invalid name value (must be a string): {k}")
            if not isinstance(v, str):
                raise ValueError(f"Invalid string value: {v}")
            letter_dict[k] = v.strip('"').strip()

        for k, v in letter_dict.items():
            if v in cls._value2member_map_:
                raise ValueError(f"Duplicate value found: {v} for {k}")
            setattr(cls, k, v)

        return cls
