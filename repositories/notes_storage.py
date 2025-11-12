from typing import Protocol
from models.note import Note


class NotesStorage(Protocol):
    def load(self) -> dict[int, Note]:
        ...

    def save(self, notes: dict[int, Note]) -> None:
        ...
