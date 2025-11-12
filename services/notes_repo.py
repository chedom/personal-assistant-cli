from typing import Optional, Iterable, Protocol, Collection
from models.note import Note, Tag


class NotesRepository(Protocol):
    """Repository for the notes"""
    def add(self, note: Note) -> None:
        """Add a note to the repository"""
        ...

    def get(self, note_id: int) -> Optional[Note]:
        """Get a note from the repository"""
        ...

    def all(self) -> Iterable[Note]:
        """Get all notes from the repository"""
        ...

    def find(self, query: str) -> Iterable[Note]:
        """Search for notes by title"""
        ...

    def find_by_tags(self, tags: Collection[Tag]) -> Iterable[Note]:
        """Search for notes by tags"""
        ...

    def delete(self, note_id: int) -> None:
        """Delete a note from the repository"""
        ...

    def save(self, note: Note) -> None:
        """Update a note in the repository"""
