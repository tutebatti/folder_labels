from config import Width, Letter

class FolderLabel:
    width: float
    letter: str
    number: int
    description: str
    items: list[str]

    def __init__(self, letter: str, number: int, description: str, items: list[str], width: str):

        if number <= 0 or number >=100:
            raise ValueError(f"Number must be between 0 and 100")

        try:
            self.letter = Letter[letter].value
        except KeyError:
            raise ValueError(f"Invalid letter. Choose from: {[e.name for e in Letter]}")

        try:
            self.width = Width[width.upper()].value
        except KeyError:
            raise ValueError(f"Invalid width. Choose from: {[e.name for e in Width]}")

        self.number = number
        self.description = description
        self.items = items
