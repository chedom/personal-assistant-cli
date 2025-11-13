from models.values import Field


class Birthday(Field):

    def __init__(self, value: str):
        # TODO: validate birthday string
        super().__init__(value)
