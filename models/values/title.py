from models.values import Field


class Title(Field):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Text couldn't be empty")

        super().__init__(value)
