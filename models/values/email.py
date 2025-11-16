import re

from models.values import Field


class Email(Field):
    def __init__(self, value: str):
        """
        Initialize the Email field with a normalized and validated email address.

        Args:
            value (str): The raw email string.
        """
        normalized_value = Email.normalize(value)
        Email.validate(normalized_value)
        super().__init__(normalized_value)

    @staticmethod
    def normalize(value: str) -> str:
        """
        Normalize the email string by stripping spaces and converting to lowercase.

        Args:
            value (str): Raw email string.

        Returns:
            str: Normalized email string.
        """
        value = value.strip()
        return value.lower()

    @staticmethod
    def validate(value: str):
        """
        Validate that the email is non-empty and matches a standard email format.

        Args:
            value (str): Normalized email string.

        Raises:
            ValueError: If the email is empty or has an invalid format.
        """
        if not value:
            raise ValueError("Email should not be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
