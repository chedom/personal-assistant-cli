from models.values import Field
from datetime import datetime, date
import re


class Birthday(Field):
    def __init__(self, value: str):
        normalized_value = Birthday.normalize(value)
        Birthday.validate(normalized_value)
        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.strip()
        value = re.sub(r"[/-]", ".", value)
        return value

    @staticmethod
    def validate(value: str):
        if not value:
            raise ValueError("Birthday should not be empty")

        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")

        today = date.today()

        if birthday > today:
            raise ValueError("Birthday cannot be in the future")
