#!/usr/bin/env python3

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Convert centimeters to points (1 cm = 28.35 points)
cm_to_points = 28.35

def create_rectangle_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Default letter size (8.5 x 11 inches in points)

    # Define rectangle size in centimeters
    rect_width = 10 * cm_to_points  # 10 cm width
    rect_height = 5 * cm_to_points  # 5 cm height

    # Draw rectangle (x, y, width, height)
    x_position = 100  # Starting x position (in points)
    y_position = height - 200  # Starting y position (in points)

    c.setStrokeColor(colors.black)
    c.setFillColor(colors.whitesmoke)
    c.rect(x_position, y_position, rect_width, rect_height, fill=1)

    # Add large letter inside the rectangle
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(x_position + rect_width / 2, y_position + rect_height - 30, "A")

    # Add number below the letter
    c.setFont("Helvetica", 24)
    c.drawCentredString(x_position + rect_width / 2, y_position + rect_height - 60, "12")

    # Add list of dashes (flush left inside the rectangle)
    c.setFont("Helvetica", 12)
    c.drawString(x_position + 10, y_position + rect_height - 100, "- Dash 1")
    c.drawString(x_position + 10, y_position + rect_height - 120, "- Dash 2")

    # Save the PDF
    c.save()

# Generate the PDF
create_rectangle_pdf("rectangle_example.pdf")
