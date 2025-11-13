import re
from models.values import Field


class Tag(Field):
    def __init__(self, tag: str):
        tag = Tag.normalize(tag)
        if not tag:
            raise ValueError("Tag couldn't be empty")

        super().__init__(tag)

    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def normalize(tag: str) -> str:
        """Normalize the tag"""
        tag = tag.strip().lower()  # "Work " -> "work"
        tag = re.sub(r"\s+", "-", tag)  # "my work" -> "my-work"
        tag = re.sub(r"[^a-z0-9\-]", "", tag)  # only allow alphanumerics/dashe
        return tag
