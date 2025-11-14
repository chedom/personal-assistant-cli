from exceptions import NotFoundError
from models.contact import Contact
from typing import Iterable

_sentinel = object()


class ContactsRepository:
    def __init__(self, storage):
        self.storage = storage
        self._contacts: dict[str, Contact] = self.storage.load() or {}

    def add(self, contact: Contact):
        self._contacts[contact.name.value] = contact

    def get(self, name: str, default=_sentinel) -> Contact:
        contact = self._contacts.get(name)

        if contact is not None:
            return contact
        if default is _sentinel:  # no default was provided
            raise NotFoundError(f"Contact: {name}")
        return default

    def delete(self, name: str):
        self._contacts.pop(name)

    def find(self, query: str) -> Iterable[Contact]:
        """Search for contact by all fields"""
        return [c for c in self._contacts.values() if c.is_matching(query)]

    def all(self) -> Iterable[Contact]:
        return list(self._contacts.values())

    def save(self):
        self.storage.save(self._contacts)
