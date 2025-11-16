import re

from models.values import Field


class Address(Field):
    def __init__(self, value: str):
        """
        Initialize the Address field.

        Args:
            value (str): The raw address string to normalize and validate.
        """
        normalized = Address.normalize(value)
        Address.validate(normalized)
        super().__init__(normalized)

    @staticmethod
    def normalize(value: str) -> str:
        """
        Clean and standardize an address string
        (trim spaces, fix punctuation, remove invalid characters).
        """
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
        """
        Validate that the address is non-empty,
        has a reasonable length, and contains letters and numbers.
        """
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
