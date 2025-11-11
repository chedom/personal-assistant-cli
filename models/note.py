from typing import Self
from datetime import datetime as DateTime
from models.values import Field, Tag, Title


class Note:
    def __init__(
        self,
        title: str,
        body: str = "",
        tags: set[Tag] | None = None,
        created_at: DateTime | None = DateTime.now(),
        updated_at: DateTime | None = None,
    ):
        self.title: Title = Title(title.strip())
        self.body: Field = Field(body.strip())
        self.tags: set[Tag] = tags if tags is not None else set()
        self.created_at: DateTime = created_at
        self.updated_at: DateTime = updated_at if updated_at is not None else created_at # noqa

    def __str__(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Body: {self.body}\n"
            f"Tags: {', '.join(self.tags)}\n"
            f"Created at: {self.created_at}\n"
            f"Updated at: {self.updated_at}"
        )

    def edit_title(self, new_title: str) -> None:
        """Edit the title of the note"""
        self.title = Title(new_title.strip())
        self.updated_at = DateTime.now()

        return self

    def edit_body(self, new_body: str) -> None:
        """Edit the body of the note"""
        self.body = Field(new_body.strip())
        self.updated_at = DateTime.now()

        return self

    def edit_tags(self, *tags: str) -> None:
        """Add tags to the note"""
        if not tags:
            return

        self.tags.clear()

        for tag in tags:
            self.tags.add(Tag(tag))

        self.updated_at = DateTime.now()

    def to_dict(self) -> dict:
        """Convert the note to a dictionary"""
        return {
            "title": self.title,
            "body": self.body,
            "tags": list(self.tags),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Convert the dictionary to a note"""
        return cls(
            title=data["title"],
            body=data["body"],
            tags=set(data["tags"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
