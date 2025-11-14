from models.values import Field
import re


class Email(Field):
    def __init__(self, value: str):
        normalized_value = Email.normalize(value)
        Email.validate(normalized_value)
        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.strip()
        return value.lower()

    @staticmethod
    def validate(value: str):
        if not value:
            raise ValueError("Email should not be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
