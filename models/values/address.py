from models.values import Field
import re


class Address(Field):
    def __init__(self, value: str):
        normalized = Address.normalize(value)
        Address.validate(normalized)
        super().__init__(normalized)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.strip()
        value = re.sub(r"\s+", " ", value)
        value = re.sub(r"[^a-zA-Zа-яА-ЯіІїЇєЄ0-9\s\.,\-/]", "", value)
        value = re.sub(r"\.+", ".", value)
        value = re.sub(r",+", ",", value)
        value = re.sub(r"\s+\.", ".", value)
        value = re.sub(r"\s+,", ",", value)
        return value

    @staticmethod
    def validate(value: str):
        if not value:
            raise ValueError("Address should not be empty")

        if len(value) < 5:
            raise ValueError("Address is too short")

        if len(value) > 200:
            raise ValueError("Address is too long")

        if not re.search(r"[a-zA-Zа-яА-ЯіІїЇєЄ]", value):
            raise ValueError("Address must contain letters")

        if not re.search(r"\d", value):
            raise ValueError("Address must contain a building number")
