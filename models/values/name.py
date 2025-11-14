from models.values import Field


class Name(Field):
    def __init__(self, value: str):
        normalized_value = Name.normalize(value)
        Name.validate(normalized_value)
        super().__init__(normalized_value)
    
    @staticmethod
    def normalize(value: str) -> str:
        value = value.strip()
        return value.capitalize()
    
    @staticmethod
    def validate(value: str):
        if not value:
            raise ValueError("Name should not be empty")

        if not all(char.isalpha() or char == ' ' for char in value):
            raise ValueError("Name can contain only letters and spaces")

        if "  " in value or value.startswith(" ") or value.endswith(" "):
            raise ValueError("Incorrect usage of spaces in name")