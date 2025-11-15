from models.values import Field
import re


class Phone(Field):
    def __init__(self, value: str):
        normalized_value = Phone.normalize(value)
        Phone.validate(normalized_value)
        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        value = re.sub(r"[^\d]", "", value)
        if (value.startswith("380")):
            value = "+" + value
        elif (value.startswith("0")):
            value = "+38" + value
        return value

    @staticmethod
    def validate(value: str):
        if not value:
            raise ValueError("Phone should not be empty")

        if not value[1:].isdigit():
            raise ValueError("Phone number can contain only digits")

        if not value.startswith("+380"):
            raise ValueError("Phone should start with +380")

        if len(value) != 13:
            raise ValueError("Phone must be 13 characters long in format +380XXXXXXXXX")
