from src.config import config


class FolderLabel:
    width: float
    letter: str
    number: int
    description: str
    items: list[str]

    def __init__(self,
                 letter: str,
                 number: int,
                 description: str,
                 items: list[str],
                 width: str):

        if number <= 0 or number >=100:
            raise ValueError(f"Number must be between 0 and 100")


        if letter not in config.letters:
            raise ValueError(f"{letter} is invalid. Choose from: {[key for key in config.letters]}")
        self.letter = letter

        if width not in config.widths:
            raise ValueError(f"Invalid width. Choose from: {[key for key in config.widths]}")
        self.width = config.widths[width]

        self.number = number
        self.description = description
        self.items = items
