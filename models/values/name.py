from models.values import Field


class Name(Field):
    def __init__(self, value: str):
        """
        Initialize the Name field after validating the input.

        Args:
            value (str): The raw name string.
        """
        Name.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value: str):
        """
        Validate that the name is non-empty, contains only letters and spaces,
        and does not have leading, trailing, or double spaces.

        Args:
            value (str): The name string to validate.

        Raises:
            ValueError: If the name is empty or contains invalid characters/spaces.
        """
        if not value:
            raise ValueError("Name should not be empty")

        if not all(char.isalpha() or char == ' ' for char in value):
            raise ValueError("Name can contain only letters and spaces")

        if "  " in value or value.startswith(" ") or value.endswith(" "):
            raise ValueError("Incorrect usage of spaces in name")
