from models.contact import Contact
from typing import Iterable


class ContactsRepository:
    def __init__(self, storage):
        self.storage = storage
        self._contacts: dict[str, Contact] = self.storage.load() or {}

    def add(self, contact: Contact):
        self._contacts[contact.name.value] = contact

    def get(self, name: str) -> Contact:
        return self._contacts.get(name)

    def delete(self, name: str):
        self._contacts.pop(name)

    def find(self, query: str) -> Iterable[Contact]:
        """Search for contact by all fields"""
        return [c for c in self._contacts.values() if c.is_matching(query)]

    def all(self) -> Iterable[Contact]:
        return list(self._contacts.values())

    def save(self):
        self.storage.save(self._contacts)
