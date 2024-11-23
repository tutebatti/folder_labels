#!/usr/bin/env python3
import csv
import sys

from src.folder_label import FolderLabel
from src.pdf_output import PdfOutput
from src.config.measures import Measures


def create_labels_from_csv(csv_file: str, outfile: str):
    pdf = PdfOutput(outfile, pagesize=Measures.papersize)
    labels: list[FolderLabel] = read_labels_from_file(csv_file)

    for label in labels:
        pdf.add_label_to_canvas(label)

    pdf.save()

def read_labels_from_file(infile: str, delimiter: str = "\t") -> list[FolderLabel]:
    labels: list[FolderLabel] = list()
    with open(infile, "r") as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            letter = row[0].strip()
            number = int(row[1].strip())
            description = row[2].strip()
            items = row[3].strip().split("#")
            width = row[4].strip()
            labels.append(FolderLabel(letter, number, description, items, width))
    return labels

def main(csv_file: str, outfile: str):
    create_labels_from_csv(csv_file, outfile)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
