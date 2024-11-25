from configparser import ConfigParser

from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics

from src.config.util import get_int, check_for_missing_section
from src.config.styles import Styles


class Measures:
    config_parser: ConfigParser()

    label_height: float
    papersize: tuple
    paperwidth: float

    x_offset: float
    y_offset: float

    max_x_offset: float

    letter_x_offset_relative_to_label_center: float
    letter_y_position: float

    number_x_offset_relative_to_label_center: float
    number_y_position: float

    description_x_offset_relative_to_label_center: float
    description_y_position: float

    items_x_offset: float
    items_y_position: float
    items_mutual_y_offset: float

    symbol_width: float

    @classmethod
    def from_ini(cls, ini_file: str):
        measures = Measures()
        
        measures.set_config_reader(ini_file)
        measures.read_general_measures_from_config()
        measures.read_general_offsets_from_config()
        measures.set_positions_from_config()

        return measures

    def set_config_reader(self, ini_file: str):
        self.config_parser = ConfigParser()
        self.config_parser.read(ini_file)
        check_for_missing_section("Measures", self.config_parser)

    def read_general_measures_from_config(self):
        self.label_height = cm * self.get_int_from_config("label_height")
        self.papersize = landscape(getattr(pagesizes, self.config_parser["Measures"].get("papersize").strip('"')))
        self.paperwidth = self.papersize[0]

    def read_general_offsets_from_config(self):
        self.x_offset = self.get_int_from_config("x_offset")
        self.y_offset = self.get_int_from_config("y_offset")
        self.max_x_offset = self.paperwidth - self.x_offset

    def set_positions_from_config(self):
        self.set_letter_position_from_config()
        self.set_number_position_from_config()
        self.set_description_position_from_config()
        self.set_items_position_from_config()

    def set_letter_position_from_config(self):
        self.letter_x_offset_relative_to_label_center = self.get_int_from_config(
            "letter_x_offset_relative_to_label_center")
        self.letter_y_position = self.y_offset + self.label_height + self.get_int_from_config("letter_y_offset")

    def set_number_position_from_config(self):
        self.number_x_offset_relative_to_label_center = self.get_int_from_config(
            "number_x_offset_relative_to_label_center")
        self.number_y_position = self.letter_y_position + self.get_int_from_config(
            "number_y_offset_relative_to_letter")

    def set_description_position_from_config(self):
        self.description_x_offset_relative_to_label_center = self.get_int_from_config(
            "description_x_offset_relative_to_label_center")
        self.description_y_position = self.letter_y_position + self.get_int_from_config(
            "description_y_offset_relative_to_letter")

    def set_items_position_from_config(self):
        self.items_x_offset = self.get_int_from_config("items_x_offset")
        self.items_y_position = self.description_y_position + self.get_int_from_config(
            "first_item_y_offset_relative_to_description")
        self.items_mutual_y_offset = self.get_int_from_config("items_mutual_y_offset")

    def calculate_symbol_width(self, styles: Styles):
        styles.register_font()

        self.symbol_width = pdfmetrics.stringWidth(
            styles.item_list_symbol,
            styles.font,
            styles.item_size
        )

    def get_int_from_config(self, key: str) -> int:
        return get_int(self.config_parser, "Measures", key)
