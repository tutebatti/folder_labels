from configparser import ConfigParser

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config.util import str_to_bool, get_int, check_for_missing_section


class Styles:
    config_parser: ConfigParser()
    
    use_custom_font: bool
    custom_font_file: str
    default_font: str
    font: str

    letter_size: int
    number_size: int
    description_size: int
    item_size: int

    item_list_symbol: str

    @classmethod
    def from_ini(cls, ini_file: str):
        styles = Styles()
        
        styles.set_config_reader(ini_file)

        styles.read_font_types_from_config()
        styles.read_font_sizes_from_config()
        styles.item_list_symbol = styles.config_parser["Styles"].get("item_list_symbol").strip('"').strip() + " "

        return styles
    
    def set_config_reader(self, ini_file: str):
        self.config_parser = ConfigParser()
        self.config_parser.read(ini_file)
        check_for_missing_section("Styles", self.config_parser)

    def read_font_types_from_config(self):
        use_custom_font = self.config_parser["Styles"].get("use_custom_font", "False")
        self.use_custom_font = str_to_bool(use_custom_font)

        self.custom_font_file = self.config_parser["Styles"].get("custom_font_file", "").strip('"').strip()
        self.default_font = self.config_parser["Styles"].get("default_font", "Helvetica").strip('"').strip()
        self.font = "custom" if self.use_custom_font else self.default_font

    def read_font_sizes_from_config(self):
        self.letter_size = self.get_int_from_config( "letter_size")
        self.number_size = self.get_int_from_config( "number_size")
        self.description_size = self.get_int_from_config( "description_size")
        self.item_size = self.get_int_from_config( "item_size")

    def get_int_from_config(self, key: str) -> int:
        return get_int(self.config_parser, "Styles", key)

    def register_font(self):
        if self.use_custom_font:
            pdfmetrics.registerFont(TTFont(name=self.font, filename=self.custom_font_file))
