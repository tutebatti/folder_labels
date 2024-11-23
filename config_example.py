from enum import Enum

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontStyles:
    use_custom_font: bool = False # set to True, if you want to use a custom font
    custom_font_file: str = "/path/to/custom/font" # best copy a ttf to the base folder and reference it with "font.ttf"
    default_font_type: str = "Helvetica" # other possible values: Courier, Times-Roman
    font_type: str = "custom" if use_custom_font else default_font_type

    letter_size: int = 48
    number_size: int = 16
    description_size: int = 20
    item_size: int = 12

    item_list_symbol: str = "–" + " " # Change to, e.g., *

    @classmethod
    def register_font(cls):
        if cls.use_custom_font:
            pdfmetrics.registerFont(TTFont(name=cls.font_type, filename=cls.custom_font_file))


class Measures:
    CM_TO_POINTS: float = 28.35 # leave unchanged

    label_height: float = CM_TO_POINTS * 19 # adapt, if necessary
    papersize: tuple[float, float] | None = landscape(A4) # adapt, if necessary
    paperwidth: float = papersize[0]

    x_offset: float = 20 # adapt, if necessary
    y_offset: float = 30 # adapt, if necessary

    max_x_offset: float = paperwidth - x_offset

    letter_x_offset_relative_to_label_center: float = -10
    letter_y_position: float = y_offset + label_height - 100

    number_x_offset_relative_to_label_center: float = 25
    number_y_position: float = letter_y_position

    description_x_offset_relative_to_label_center: float = 0
    description_y_position: float = letter_y_position - 50

    items_x_offset: float = 20
    items_y_position: float = description_y_position - 50
    items_mutual_y_offset: float = 20

    symbol_width: float

    @classmethod
    def calculate_symbol_width(cls):
        FontStyles.register_font()

        cls.symbol_width = pdfmetrics.stringWidth(
            FontStyles.item_list_symbol,
            FontStyles.font_type,
            FontStyles.item_size
        )



class Width(Enum):
    WIDE: float = Measures.CM_TO_POINTS * 5.6 # adapt, if necessary
    NARROW: float = Measures.CM_TO_POINTS * 3 # adapt, if necessary


# adapt this (except if you're Batman and Robin)
class Letter(Enum):
    Batman = "B"
    Robin = "R"
    Team = "T"
