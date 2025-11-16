import re

from models.values import Field


class Tag(Field):
    def __init__(self, tag: str):
        """
        Initialize the Tag field with a normalized, non-empty tag string.

        Args:
            tag (str): Raw tag string.

        Raises:
            ValueError: If the normalized tag is empty.
        """
        tag = Tag.normalize(tag)
        if not tag:
            raise ValueError("Tag couldn't be empty")

        super().__init__(tag)

    def __hash__(self) -> int:
        """
        Return a hash of the tag to allow usage in sets and as dict keys.

        Returns:
            int: Hash value of the tag string.
        """
        return hash(self.value)

    @staticmethod
    def normalize(tag: str) -> str:
        """Normalize the tag"""
        tag = tag.strip().lower()  # "Work " -> "work"
        tag = re.sub(r"\s+", "-", tag)  # "my work" -> "my-work"
        tag = re.sub(r"[^a-z0-9\-]", "", tag)  # only allow alphanumerics/dashe
        return tag
