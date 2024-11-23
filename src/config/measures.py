import configparser
from configparser import ConfigParser

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics

from src.config.util import get_int
from src.config.styles import Styles


class Measures:
    CM_TO_POINTS: float = 28.35 # leave unchanged

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
    def calculate_symbol_width(cls):
        Styles.register_font()

        cls.symbol_width = pdfmetrics.stringWidth(
            Styles.item_list_symbol,
            Styles.font,
            Styles.item_size
        )

    @classmethod
    def from_ini(cls, ini_file: str):
        config_parser = configparser.ConfigParser()
        config_parser.read(ini_file)

        measures = Measures()

        measures.read_general_measures_from_config(config_parser)

        measures.read_general_offsets_from_config(config_parser)
        measures.set_positions(config_parser)


        return measures

    def read_general_measures_from_config(self, config_parser):
        self.label_height = Measures.CM_TO_POINTS * get_int(config_parser, "Measures", "label_height")
        self.papersize = landscape(A4)  # TODO
        self.paperwidth = self.papersize[0]

    def read_general_offsets_from_config(self, config_parser: ConfigParser):
        self.x_offset = get_int(config_parser, "Measures", "x_offset")
        self.y_offset = get_int(config_parser, "Measures", "y_offset")
        self.max_x_offset = self.paperwidth - self.x_offset

    def set_positions(self, config_parser: ConfigParser):
        self.set_letter_position_from_config(config_parser)
        self.set_number_position_from_config(config_parser)
        self.set_description_position_from_config(config_parser)
        self.set_items_position_from_config(config_parser)

    def set_letter_position_from_config(self, config_parser: ConfigParser):
        self.letter_x_offset_relative_to_label_center = get_int(config_parser, "Measures",
                                                                "letter_x_offset_relative_to_label_center")
        self.letter_y_position = self.y_offset + self.label_height + get_int(config_parser, "Measures",
                                                                             "letter_y_offset")

    def set_number_position_from_config(self, config_parser: ConfigParser):
        self.number_x_offset_relative_to_label_center = get_int(config_parser, "Measures",
                                                                "number_x_offset_relative_to_label_center")
        self.number_y_position = self.letter_y_position + get_int(config_parser, "Measures",
                                                                  "number_y_offset_relative_to_letter")

    def set_description_position_from_config(self, config_parser: ConfigParser):
        self.description_x_offset_relative_to_label_center = get_int(config_parser, "Measures",
                                                                     "description_x_offset_relative_to_label_center")
        self.description_y_position = self.letter_y_position + get_int(config_parser, "Measures",
                                                                       "description_y_offset_relative_to_letter")

    def set_items_position_from_config(self, config_parser: ConfigParser):
        self.items_x_offset = get_int(config_parser, "Measures", "items_x_offset")
        self.items_y_position = self.description_y_position + get_int(config_parser, "Measures",
                                                                      "first_item_y_offset_relative_to_description")
        self.items_mutual_y_offset = get_int(config_parser, "Measures", "items_mutual_y_offset")
