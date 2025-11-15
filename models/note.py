from typing import Self, Collection
from datetime import datetime as DateTime
from models.values import Field, Tag, Title
from ui.output_util import Out


class Note:
    short_text_len = 30

    def __init__(
        self,
        note_id: int,
        title: str,
        body: str = "",
        tags: set[Tag] | None = None,
        created_at: DateTime | None = DateTime.now(),
        updated_at: DateTime | None = None,
    ):
        self.__title: Title = Title(title.strip())
        self.__body: Field = Field(body.strip())
        self.__tags: set[Tag] = tags if tags is not None else set()
        self.__note_id: int = note_id
        self.__created_at: DateTime = created_at
        self.__updated_at: DateTime = updated_at if updated_at is not None else created_at # noqa

    def __str__(self) -> str:
        tags_str = ",".join([str(t) for t in self.__tags]) if self.__tags else "—"
        return (
            f"{Out.SECTION}Note:{Out.RESET}\n"
            f"{Out.PARAM} > ID: {Out.INFO}{self.__note_id}{Out.RESET}\n"
            f"{Out.PARAM} > Title: {Out.INFO}{self.__title}{Out.RESET}\n"
            f"{Out.PARAM} > Body: {Out.INFO}{self.__body}{Out.RESET}\n"
            f"{Out.PARAM} > Tags: {Out.INFO}{tags_str}{Out.RESET}\n"
            f"{Out.PARAM} > Created at: "
            f"{Out.INFO}{self.__created_at:%d.%m.%Y}{Out.RESET}\n"
            f"{Out.PARAM} > Updated at: "
            f"{Out.INFO}{self.__updated_at:%d.%m.%Y}{Out.RESET}"
        )

    # flake8: noqa: E501 Line too long
    def preview(self) -> str:
        """Get a preview of the note"""
        tags_str = ",".join([v.value for v in self.__tags]) if self.__tags else "—"
        return (
            f"{Out.SECTION}Note #{self.__note_id} ({self.__updated_at:%d.%m.%Y}): "
            f"{Out.INFO}{self.field_preview(self.__title)}\n"
            f"{Out.PARAM}Body: {Out.INFO}{self.field_preview(self.__body)}\n"
            f"{Out.PARAM}Tags: {Out.INFO}{tags_str}\n"
        )

    @property
    def note_id(self) -> int:
        """Get the note id"""
        return self.__note_id

    @property
    def updated_at(self) -> DateTime:
        """Get the updated at date"""
        return self.__updated_at

    @property
    def created_at(self) -> DateTime:
        """Get the created at date"""
        return self.__created_at

    @property
    def tags(self) -> set[Tag]:
        """Get the tags"""
        return self.__tags

    @property
    def title(self) -> Title:
        """Get the title"""
        return self.__title

    @property
    def body(self) -> Field:
        """Get the body"""
        return self.__body

    def contains(self, substr: str) -> bool:
        """Check if the note contains a substring"""
        substr = substr.strip().lower()
        return substr in self.__title.value.lower() \
            or substr in self.__body.value.lower()

    def count_matching_tags(self, tags: Collection[Tag]) -> int:
        """Count the number of matching tags"""
        return len(self.__tags & set(tags))

    def edit_note(
        self,
        new_title: str = None,
        new_body: str = None,
        new_tags: set[Tag] = None,
    ):
        """Edit the note"""
        if new_title is not None:
            self.__title = Title(new_title.strip())

        if new_body is not None:
            self.__body = Field(new_body.strip())

        if new_tags is not None:
            self.__tags = new_tags

        self.__updated_at = DateTime.now()

        return self

    def to_dict(self) -> dict:
        """Convert the note to a dictionary"""
        # Sort tags to make it stable
        tags = [v.value for v in self.__tags]
        tags.sort()

        return {
            "title": self.__title.value,
            "body": self.__body.value,
            "tags": tags,
            "note_id": self.__note_id,
            "created_at": self.__created_at.isoformat(),
            "updated_at": self.__updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Convert the dictionary to a note"""
        tags = {Tag(t) for t in data["tags"]}
        return cls(
            note_id=data["note_id"],
            title=data["title"],
            body=data["body"],
            tags=tags,
            created_at=DateTime.fromisoformat(data["created_at"]),
            updated_at=DateTime.fromisoformat(data["updated_at"]),
        )

    @classmethod
    def field_preview(cls, field: Field) -> str:
        """Get a preview of the field"""
        return field.value.split("\n", 1)[0][:cls.short_text_len]
