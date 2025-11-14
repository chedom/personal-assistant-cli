from typing import Optional, Iterable, Collection
from models.note import Note, Tag
from exceptions import NotFoundError
from repositories.storage import Storage

_sentinel = object()


class NotesInMemoryRepository:
    """Repository for the notes"""
    def __init__(self, storage: Storage[Note]) -> None:
        self.__storage: Storage[Note] = storage
        self.__notes: dict[int, Note] = storage.load() or {}
        self.last_id = max(self.__notes, default=0)

    def add(self, note: Note) -> None:
        """Add a note to the repository"""
        self.__notes[note.note_id] = note

    def get(self, note_id: int, default=_sentinel) -> Optional[Note]:
        """Get a note from the repository"""
        note = self.__notes.get(note_id)

        if note is not None:
            return note
        if default is _sentinel:  # no default was provided
            raise NotFoundError(f"Note: {note_id}")
        return default

    def all(self) -> Iterable[Note]:
        return list(self.__notes.values())

    def find(self, query: str) -> Iterable[Note]:
        """Search for notes by title"""
        return [n for n in self.__notes.values() if n.contains(query)]

    def find_by_tags(self, tags: Collection[Tag]) -> Iterable[Note]:
        """Search for notes by tags"""
        return [
            n for n in self.__notes.values()
            if n.count_matching_tags(tags) > 0
        ]

    def delete(self, note_id: int) -> None:
        """Delete a note from the repository"""
        self.__notes.pop(note_id, None)

    def save(self) -> None:
        """Update a note in the repository"""
        # is not relevant for inmemory storage,
        # relevant for DBMS (Mongo, Postgresql, etc) adapter
        ...

    def generate(self) -> int:
        self.last_id += 1
        return self.last_id

    def flush(self) -> None:
        self.__storage.save(self.__notes)
