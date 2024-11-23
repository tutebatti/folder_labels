from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from src.config import FontStyles
from src.config.measures import Measures
from src.folder_label import FolderLabel


def determine_scale_factor(string: str, fontsize: int, max_width: float) -> float:
    string_width: float = pdfmetrics.stringWidth(string, FontStyles.font_type, fontsize)
    return max_width / string_width * 0.9 if string_width >= max_width else 1


class PdfOutput(canvas.Canvas):
    x_offset: float = Measures.x_offset

    def add_label_to_canvas(self, label: FolderLabel) -> None:
        self.prepare_for_label(label)
        self.add_label_data(label)
        self.x_offset += label.width

    def prepare_for_label(self, label):
        FontStyles.register_font()
        self.setStrokeColor(colors.black)
        self.add_pagebreak_if_necessary(next_label=label)
        self.add_rectangle(width=label.width)

    def add_pagebreak_if_necessary(self, next_label: FolderLabel) -> None:
        if self.x_offset + next_label.width > Measures.max_x_offset:
            self.x_offset = 20
            self.showPage()

    def add_rectangle(self, width: float) -> None:
        self.rect(x=self.x_offset, y=Measures.y_offset, width=width, height=Measures.label_height, fill=0)

    def add_label_data(self, label: FolderLabel) -> None:
        self.add_letter(letter=label.letter, label_width=label.width)
        self.add_number(number=label.number, label_width=label.width)
        self.add_description(description=label.description, label_width=label.width)
        self.add_items(items=label.items, label_width=label.width)

    def add_letter(self, letter: str, label_width: float) -> None:
        self.setFont(FontStyles.font_type, FontStyles.letter_size)
        self.drawCentredString(x=self.x_offset + label_width / 2 + Measures.letter_x_offset_relative_to_label_center,
                               y=Measures.letter_y_position,
                               text=letter)

    def add_number(self, number: int, label_width: float) -> None:
        self.setFont(FontStyles.font_type, FontStyles.number_size)
        self.drawCentredString(
            x=self.x_offset + label_width / 2 + Measures.number_x_offset_relative_to_label_center,
            y=Measures.number_y_position,
            text=f"{number:02}")

    def add_description(self, description: str, label_width: float) -> None:
        scale_factor: float = determine_scale_factor(
            string=description,
            fontsize=FontStyles.description_size,
            max_width=label_width - 10)
        self.setFont(FontStyles.font_type, FontStyles.description_size * scale_factor)
        self.drawCentredString(
            x=self.x_offset + label_width / 2 + Measures.description_x_offset_relative_to_label_center,
            y=Measures.description_y_position,
            text=description)

    def add_items(self, items: list[str], label_width: float) -> None:
        Measures.calculate_symbol_width()
        for idx, item in enumerate(items):
            self.add_list_symbol(idx)
            self.add_item(idx, item, label_width)

    def add_list_symbol(self, idx: int) -> None:
        self.setFont(FontStyles.font_type, FontStyles.item_size)
        self.drawString(x=self.x_offset + Measures.items_x_offset,
                        y=Measures.items_y_position - Measures.items_mutual_y_offset * idx,
                        text=FontStyles.item_list_symbol)

    def add_item(self, idx: int, item: str, label_width: float):
        scale_factor: float = determine_scale_factor(
            string=FontStyles.item_list_symbol + item,
            fontsize=FontStyles.item_size,
            max_width=label_width - Measures.items_x_offset - Measures.symbol_width)
        self.setFont(FontStyles.font_type, FontStyles.item_size * scale_factor)
        self.drawString(x=self.x_offset + Measures.items_x_offset + Measures.symbol_width,
                        y=Measures.items_y_position - Measures.items_mutual_y_offset * idx,
                        text=item)
