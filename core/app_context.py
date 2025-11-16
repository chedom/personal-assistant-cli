from services.contacts_service import ContactsService
from services.notes_service import NotesService


class AppContext:
    """
    Application context DI instances.

    Attributes:
        contacts (ContactsService): Service for managing contacts.
        notes (NotesService): Service for managing notes.
    """
    def __init__(self, contacts_service: ContactsService, notes_service: NotesService):
        self.contacts = contacts_service
        self.notes = notes_service
