from enum import Enum
from repositories import NotesInMemoryRepository, ContactsInMemoryRepository
from storage import FileStorage, JsonSerializer, PickleSerializer
from models import Note, Contact


class SerializerType(Enum):
    JSON = "json"
    PICKLE = "pickle"


def create_notes_repo(
        filename: str,
        serializer_type: SerializerType = SerializerType.PICKLE
) -> NotesInMemoryRepository:
    """Create a notes repository"""

    match serializer_type:
        case SerializerType.JSON:
            notes_serializer = JsonSerializer[int, Note](
                to_dict=Note.to_dict,
                from_dict=Note.from_dict,
                to_key=str,
                from_key=int,
            )
        case SerializerType.PICKLE:
            notes_serializer = PickleSerializer()
        case _:
            raise ValueError(f"Unknown serializer: {serializer_type}")

    notes_file_storage = FileStorage[int, Note](filename, notes_serializer)

    return NotesInMemoryRepository(notes_file_storage)


def create_contacts_repo(
        filename: str,
        serializer_type: SerializerType = SerializerType.PICKLE
) -> ContactsInMemoryRepository:
    """Create a contacts repository"""

    match serializer_type:
        case SerializerType.JSON:
            contacts_serializer = JsonSerializer[str, Contact](
                to_dict=Contact.to_dict,
                from_dict=Contact.from_dict,
            )
        case SerializerType.PICKLE:
            contacts_serializer = PickleSerializer()
        case _:
            raise ValueError(f"Unknown serializer: {serializer_type}")

    contacts_file_storage = FileStorage[str, Contact](filename, contacts_serializer)

    return ContactsInMemoryRepository(contacts_file_storage)
