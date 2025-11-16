from models.values import Field


class Title(Field):
    def __init__(self, value: str):
        """
        Initialize the Title field with a non-empty string.

        Args:
            value (str): The text value for the title.

        Raises:
            ValueError: If the provided value is empty.
        """
        if not value:
            raise ValueError("Text couldn't be empty")

        super().__init__(value)
