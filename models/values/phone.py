import re

from models.values import Field


class Phone(Field):
    def __init__(self, value: str):
        """
        Initialize the Phone field with a normalized and validated phone number.

        Args:
            value (str): The raw phone number string.
        """
        normalized_value = Phone.normalize(value)
        Phone.validate(normalized_value)
        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        """
        Normalize a phone number by removing non-digit characters and
        converting it to the standard format starting with +380.

        Args:
            value (str): Raw phone number string.

        Returns:
            str: Normalized phone number in format +380XXXXXXXXX.
        """
        value = re.sub(r"[^\d]", "", value)
        if value.startswith("380"):
            value = "+" + value
        elif value.startswith("0"):
            value = "+38" + value
        return value

    @staticmethod
    def validate(value: str):
        """
        Validate that the phone number is non-empty, contains only digits,
        starts with +380, and has a correct length.

        Args:
            value (str): Normalized phone number string.

        Raises:
            ValueError: If the phone number is empty, invalid, or incorrectly formatted.
        """
        if not value:
            raise ValueError("Phone should not be empty")

        if not value[1:].isdigit():
            raise ValueError("Phone number can contain only digits")

        if not value.startswith("+380"):
            raise ValueError("Phone should start with +380")

        if len(value) != 13:
            raise ValueError("Phone must be 13 characters long in format +380XXXXXXXXX")
