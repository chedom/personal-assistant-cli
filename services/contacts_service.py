from typing import Optional, Iterable
from repositories.contacts import ContactsRepository
from models import Contact
from models.values import Email, Phone, Address, Birthday


class ContactsService:
    def __init__(self, repo: ContactsRepository):
        self.repo = repo

    def add_contact(self, name: str, phone: str) -> Contact:
        new_contact = Contact(name)
        new_contact.add_phone(Phone(phone))

        self.repo.add(new_contact)
        self.repo.save()
        return new_contact

    def get(self, name: str) -> Contact | None:
        return self.repo.get(name)

    def add_phone(self, name: str, phone: str) -> bool:
        existing_contact = self.repo.get(name, default=None)
        if existing_contact:
            existing_contact.add_phone(Phone(phone))
            self.repo.save()
            return True
        return False

    def set_email(self, name: str, raw_email: Optional[str]):
        contact = self.repo.get(name)
        email = None

        if raw_email is not None:
            email = Email(raw_email)

        contact.set_email(email)
        self.repo.save()

    def set_birthday(self, name: str, raw_birthday: Optional[str]):
        contact = self.repo.get(name)
        birthday = None

        if raw_birthday is not None:
            birthday = Birthday(raw_birthday)

        contact.set_birthday(birthday)
        self.repo.save()

    def set_address(self, name: str, raw_address: Optional[str]):
        contact = self.repo.get(name)
        address = None
        if raw_address is not None:
            address = Address(raw_address)

        contact.set_address(address)
        self.repo.save()

    def edit_phone(self, name: str, prev_phone: str, new_phone: str) -> None:
        contact = self.repo.get(name)
        contact.edit_phone(Phone(prev_phone), Phone(new_phone))
        self.repo.save()  # should it be ?

    def find(self, search: str) -> Iterable[Contact]:
        return self.repo.find(search)

    def all(self) -> Iterable[Contact]:
        return self.repo.all()

    # TODO: implement other methods to deal with contacts service
