import re
from datetime import datetime, date

from models.values import Field


class Birthday(Field):
    def __init__(self, value: str):
        """
        Initialize the Birthday field with a normalized and validated date.

        Args:
            value (str): The raw birthday string in format DD.MM.YYYY (or with / or -).
        """
        normalized_value = Birthday.normalize(value)
        Birthday.validate(normalized_value)
        super().__init__(
            datetime.strptime(normalized_value, "%d.%m.%Y").strftime("%d.%m.%Y")
        )

    @staticmethod
    def normalize(value: str) -> str:
        """
        Normalize a birthday string by stripping spaces and
        replacing separators with dots.

        Args:
            value (str): Raw birthday string.

        Returns:
            str: Normalized birthday string in format DD.MM.YYYY.
        """
        value = value.strip()
        value = re.sub(r"[/-]", ".", value)
        return value

    @staticmethod
    def validate(value: str):
        """
        Validate that the birthday is non-empty, correctly formatted,
        represents a real calendar date, and is not in the future.

        Args:
            value (str): Normalized birthday string.

        Raises:
            ValueError: If the birthday is empty, incorrectly formatted,
            invalid, or in the future.
        """
        if not value:
            raise ValueError("Birthday should not be empty")

        if not re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", value):
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        day_str, month_str, _ = value.split(".")
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
