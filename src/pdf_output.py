from reportlab.lib import colors
from reportlab.pdfgen import canvas

from src.config import config
from src.config.util import determine_scale_factor
from src.folder_label import FolderLabel


class PdfOutput(canvas.Canvas):
    x_offset: float = config.measures.x_offset

    def add_label_to_canvas(self, label: FolderLabel) -> None:
        self.prepare_for_label(label)
        self.add_label_data(label)
        self.x_offset += label.width

    def prepare_for_label(self, label):
        self.setStrokeColor(colors.black)
        self.add_pagebreak_if_necessary(next_label=label)
        self.add_rectangle(width=label.width)

    def add_pagebreak_if_necessary(self, next_label: FolderLabel) -> None:
        if self.x_offset + next_label.width > config.measures.max_x_offset:
            self.x_offset = 20
            self.showPage()

    def add_rectangle(self, width: float) -> None:
        self.rect(x=self.x_offset, y=config.measures.y_offset, width=width, height=config.measures.label_height, fill=0)

    def add_label_data(self, label: FolderLabel) -> None:
        self.add_letter(letter=label.letter, label_width=label.width)
        self.add_number(number=label.number, label_width=label.width)
        self.add_description(description=label.description, label_width=label.width)
        self.add_items(items=label.items, label_width=label.width)

    def add_letter(self, letter: str, label_width: float) -> None:
        self.setFont(config.styles.font, config.styles.letter_size)
        self.drawCentredString(x=self.x_offset + label_width / 2 + config.measures.letter_x_offset_relative_to_label_center,
                               y=config.measures.letter_y_position,
                               text=config.letters[letter])

    def add_number(self, number: int, label_width: float) -> None:
        self.setFont(config.styles.font, config.styles.number_size)
        self.drawCentredString(
            x=self.x_offset + label_width / 2 + config.measures.number_x_offset_relative_to_label_center,
            y=config.measures.number_y_position,
            text=f"{number:02}")

    def add_description(self, description: str, label_width: float) -> None:
        scale_factor: float = determine_scale_factor(
            string=description,
            fontsize=config.styles.description_size,
            max_width=label_width - 10)
        self.setFont(config.styles.font, config.styles.description_size * scale_factor)
        self.drawCentredString(
            x=self.x_offset + label_width / 2 + config.measures.description_x_offset_relative_to_label_center,
            y=config.measures.description_y_position,
            text=description)

    def add_items(self, items: list[str], label_width: float) -> None:
        for idx, item in enumerate(items):
            self.add_list_symbol(idx)
            self.add_item(idx, item, label_width)

    def add_list_symbol(self, idx: int) -> None:
        self.setFont(config.styles.font, config.styles.item_size)
        self.drawString(x=self.x_offset + config.measures.items_x_offset,
                        y=config.measures.items_y_position - config.measures.items_mutual_y_offset * idx,
                        text=config.styles.item_list_symbol)

    def add_item(self, idx: int, item: str, label_width: float):
        scale_factor: float = determine_scale_factor(
            string=config.styles.item_list_symbol + item,
            fontsize=config.styles.item_size,
            max_width=label_width - config.measures.items_x_offset - config.measures.symbol_width)
        self.setFont(config.styles.font, config.styles.item_size * scale_factor)
        self.drawString(x=self.x_offset + config.measures.items_x_offset + config.measures.symbol_width,
                        y=config.measures.items_y_position - config.measures.items_mutual_y_offset * idx,
                        text=item)
