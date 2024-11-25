from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

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
            self.x_offset = config.measures.x_offset
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
        letter_x_position: float = (self.x_offset
                                    + label_width / 2
                                    + config.measures.letter_x_offset_relative_to_label_center)
        self.drawCentredString(x=letter_x_position,
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
            max_width=label_width * config.measures.max_width_factor)
        self.setFont(config.styles.font, config.styles.description_size * scale_factor)
        self.drawCentredString(
            x=self.x_offset + label_width / 2 + config.measures.description_x_offset_relative_to_label_center,
            y=config.measures.description_y_position,
            text=description)

    def add_items(self, items: list[str], label_width: float) -> None:
        items_text = '<br/>'.join([config.styles.item_list_symbol + chr(160) + item for item in items])

        styles = getSampleStyleSheet()
        item_style = styles['Normal']
        item_style.fontName = config.styles.font
        item_style.fontSize = config.styles.item_size
        item_style.leading = config.styles.item_spacing

        item_paragraph = Paragraph(items_text, item_style)

        item_paragraph_width = label_width - 2 * config.measures.items_x_offset
        item_paragraph.wrapOn(self, item_paragraph_width, config.measures.label_height)

        item_paragraph_x_position = self.x_offset + config.measures.items_x_offset
        item_paragraph_y_position = config.measures.items_y_position - item_paragraph.height

        item_paragraph.drawOn(self, item_paragraph_x_position, item_paragraph_y_position)

        # # Translate the canvas 45 degrees
        # c.translate(x_position + 10, y_position)  # Move the origin to the right of the bullet
        # c.rotate(45)
        # # Draw the rotated text
        # c.drawString(0, 0, bullet)  # Text is drawn at the new rotated position
        # # Restore the canvas state (so rotation doesn't affect subsequent elements)
        # c.restoreState()
