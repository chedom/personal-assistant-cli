from repositories import NotesInMemoryRepository, ContactsInMemoryRepository
from storage import FileStorage, JsonSerializer
from models import Note, Contact


def create_notes_repo(filepath: str) -> NotesInMemoryRepository:
    """Create a notes repository"""
    notes_serializer = JsonSerializer[int, Note](
        to_dict=Note.to_dict,
        from_dict=Note.from_dict,
        to_key=str,
        from_key=int,
    )
    notes_file_storage = FileStorage[int, Note](filepath, notes_serializer)

    return NotesInMemoryRepository(notes_file_storage)


def create_contacts_repo(filepath: str) -> ContactsInMemoryRepository:
    """Create a contacts repository"""
    contacts_serializer = JsonSerializer[str, Contact](
        to_dict=Contact.to_dict,
        from_dict=Contact.from_dict,
    )
    contacts_file_storage = FileStorage[str, Contact](filepath, contacts_serializer)

    return ContactsInMemoryRepository(contacts_file_storage)
