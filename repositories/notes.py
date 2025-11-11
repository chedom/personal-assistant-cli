from typing import Protocol, Optional, Iterable
from models.note import Note, Title, Tag


class NotesRepository(Protocol):
    """Interface for the notes repository"""
    def add(self, note: Note) -> None:
        """Add a note to the repository"""
        ...

    def get(self, title: Title) -> Optional[Note]:
        """Get a note from the repository"""
        ...

    def all(self) -> Iterable[Note]:
        """Get all notes from the repository"""
        ...

    def find_by_title(self, title_query: str)-> Iterable[Note]:
        """Search for notes by title"""
        ...

    def find_by_tags(self, *tags: Tag) -> Iterable[Note]:
        """Search for notes by tags"""
        ...

    def save(self, note: Note) -> None:
        """Update a note in the repository"""
        ...

    def delete(self, title: Title) -> None:
        """Delete a note from the repository"""
        ...

