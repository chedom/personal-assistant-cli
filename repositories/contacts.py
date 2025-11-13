from models.contact import Contact


class ContactsRepository:
    def __init__(self, storage):
        self.storage = storage
        self._contacts: dict[str, Contact] = self.storage.load() or {}  # should be dictionary


    def add(self, contact: Contact):
        self._contacts[contact.name.value] = contact


    def get(self, name : str) -> Contact:
        return self._contacts.get(name)


    def delete(self, name : str):
        self._contacts.pop(name)


    # TODO: Implement other methods that works with collection

    def all(self):
        return self._contacts
    

    def save(self):
        self.storage.save(self._contacts)
