from typing import Iterable
from models.contact import Contact
from exceptions import AlreadyExistError, NotFoundError
from repositories.storage import Storage

_sentinel = object()


class ContactsInMemoryRepository:
    """Inmemory repository for the contacts"""
    def __init__(self, storage: Storage[str, Contact]) -> None:
        self.__storage: Storage[str, Contact] = storage
        self.__contacts: dict[str, Contact] = storage.load() or {}

    def add(self, contact: Contact) -> None:
        """Add a contact to the repository"""
        if self.__contacts.get(contact.name.value) is not None:
            raise AlreadyExistError(f"Contact {contact.name.value}")

        self.__contacts[contact.name.value] = contact

    def get(self, name: str, default=_sentinel) -> Contact:
        """Get a contact from the repository"""
        contact = self.__contacts.get(name)

        if contact is not None:
            return contact
        if default is _sentinel:  # no default was provided
            raise NotFoundError(f"Contact: {name}")
        return default

    def delete(self, name: str):
        """Delete a contact from the repository"""
        self.__contacts.pop(name)

    def find(self, query: str) -> Iterable[Contact]:
        """Search for contact by all fields"""
        return [c for c in self.__contacts.values() if c.is_matching(query)]

    def all(self) -> Iterable[Contact]:
        """Get all contacts from the repository"""
        return list(self.__contacts.values())

    def save(self, contact: Contact) -> None:
        # is not relevant for inmemory storage,
        # relevant for DBMS (Mongo, Postgresql, etc) adapter
        ...

    def flush(self) -> None:
        """Flush the repository to the storage"""
        self.__storage.save(self.__contacts)
