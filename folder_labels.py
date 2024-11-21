#!/usr/bin/env python3
import csv
import sys
from enum import Enum

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

CM_TO_POINTS: float = 28.35

class FolderLabel:
    width: float
    letter: str
    number: int
    label: str
    items: list[str]

    class Width(Enum):
        WIDE = 5.6
        NARROW = 3

    class Letter(Enum):
        L = "L"
        A = "A"
        F = "F"
        S = "S"

    HEIGHT: float = 19 * CM_TO_POINTS

    def __init__(self, letter: str, number: int, label: str, items: list[str], width: str):

        if number <= 0 or number >=100:
            raise ValueError(f'Number must be between 0 and 100')

        try:
            self.letter = self.Letter[letter.upper()].value
        except KeyError:
            raise ValueError(f"Invalid letter. Choose from: {[e.name for e in self.Letter]}")

        try:
            self.width = self.Width[width.upper()].value
        except KeyError:
            raise ValueError(f"Invalid width. Choose from: {[e.name for e in self.Width]}")

        self.number = number
        self.label = label
        self.items = items


class PdfPage(canvas.Canvas):
    x_offset: float = 20
    max_x_offset = landscape(A4)[0] - 20
    y_offset: float = 30

    def add_label_to_canvas(self, label: FolderLabel) -> None:

        self.setStrokeColor(colors.black)

        # Add pagebreak if necessary

        if self.x_offset + label.width > self.max_x_offset:
            self.x_offset = 20
            self.showPage()

        # Add rectangle
        rect_width = label.width * CM_TO_POINTS
        self.rect(self.x_offset, self.y_offset, rect_width, FolderLabel.HEIGHT, fill=0)

        # Add letter
        self.setFont("Helvetica", 48)
        letter_x_pos: float = self.x_offset + rect_width / 2 - 10
        letter_y_pos: float = self.y_offset + FolderLabel.HEIGHT - 60
        self.drawCentredString(letter_x_pos , letter_y_pos, text=label.letter)

        # Add number next to the letter
        self.setFont("Helvetica", 16)
        number_x_pos: float = letter_x_pos + 30
        self.drawCentredString(number_x_pos, letter_y_pos, text=f"{label.number:02}")

        # Add label below the letter with number
        self.setFont("Helvetica", 20)
        label_x_pos: float = self.x_offset + rect_width / 2
        label_y_pos: float = letter_y_pos - 50
        self.drawCentredString(label_x_pos, label_y_pos, label.label)

        self.setFont("Helvetica", 12)
        items_position: float = label_y_pos - 50
        for idx, item in enumerate(label.items):
                self.drawString(self.x_offset + 10, items_position - 20 * idx, f"– {item}")

        self.x_offset += rect_width

def create_labels_from_csv(csv_file: str, outfile: str):
    pdf = PdfPage(outfile, pagesize=landscape(A4))
    labels: list[FolderLabel] = read_labels_from_file(csv_file)

    for label in labels:
        pdf.add_label_to_canvas(label)

    pdf.save()

def read_labels_from_file(infile: str) -> list[FolderLabel]:
    labels: list[FolderLabel] = list()
    with open(infile, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            letter = row[0].strip()
            number = int(row[1].strip())
            label = row[2].strip()
            items = row[3].strip().split("#")
            width = row[4].strip()
            labels.append(FolderLabel(letter, number, label, items, width))
    return labels

def main(csv_file, outfile: str):
    create_labels_from_csv(csv_file, outfile)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])