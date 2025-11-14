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

        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value):
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        
        day_str, month_str = value.split(".")
        day = int(day_str)
        month = int(month_str)

        if not 1 <= day <= 31:
            raise ValueError("Day must be between 01 and 31")
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 01 and 12")

        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid calendar date")

        today = date.today()

        if birthday > today:
            raise ValueError("Birthday cannot be in the future")
