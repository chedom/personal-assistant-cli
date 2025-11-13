from repositories import NotesInMemoryRepository
from storage import FileStorage, JsonSerializer

from models import Note


def create_notes_repo(filepath: str) -> NotesInMemoryRepository:
    notes_serializer = JsonSerializer[Note](
        to_dict=Note.to_dict,
        from_dict=Note.from_dict
    )
    notes_file_storage = FileStorage[Note](filepath, notes_serializer)
    return NotesInMemoryRepository(notes_file_storage)
