from typing import Optional, Iterable, Collection
from models.note import Note, Tag
from repositories.notes_storage import NotesStorage


class NotesInMemoryRepository:
    """Repository for the notes"""
    def __init__(self, storage: NotesStorage) -> None:
        self.__storage: NotesStorage = storage
        self.__notes: dict[int, Note] = self.__storage.load() or []
        self.last_id = max(self.__notes, default=0)

    def add(self, note: Note) -> None:
        """Add a note to the repository"""
        self.__notes[note.note_id] = note

    def get(self, note_id: int) -> Optional[Note]:
        """Get a note from the repository"""
        return self.__notes.get(note_id)

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
        
    def get_next_note_id(self) -> int:
        self.last_id += 1
        return self.last_id

    def flush(self) -> None:
        self.__storage.save(self.__notes)

