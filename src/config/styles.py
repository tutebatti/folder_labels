import configparser
from configparser import ConfigParser

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config.util import str_to_bool, get_int


class Styles:
    use_custom_font: bool
    custom_font_file: str
    default_font: str
    font: str

    letter_size: int
    number_size: int
    description_size: int
    item_size: int

    item_list_symbol: str

    def register_font(self):
        if self.use_custom_font:
            pdfmetrics.registerFont(TTFont(name=self.font, filename=self.custom_font_file))

    @classmethod
    def from_ini(cls, ini_file: str):
        config_parser = configparser.ConfigParser()
        config_parser.read(ini_file)

        styles = Styles()

        styles.read_font_types_from_config(config_parser)
        styles.read_font_sizes_from_config(config_parser)
        styles.item_list_symbol = config_parser["FontStyles"].get("item_list_symbol") + " "

        return styles

    def read_font_types_from_config(self, config_parser: ConfigParser):
        use_custom_font = config_parser["FontStyles"].get("use_custom_font", "False")
        self.use_custom_font = str_to_bool(use_custom_font)

        self.custom_font_file = config_parser["FontStyles"].get("custom_font_file", "")
        self.default_font = config_parser["FontStyles"].get("default_font", "Helvetica")
        self.font = "custom" if self.use_custom_font else self.default_font

    def read_font_sizes_from_config(self, config_parser: ConfigParser):
        self.letter_size = get_int(config_parser, "FontStyles", "letter_size")
        self.number_size = get_int(config_parser, "FontStyles", "number_size")
        self.description_size = get_int(config_parser, "FontStyles", "description_size")
        self.item_size = get_int(config_parser, "FontStyles", "item_size")
