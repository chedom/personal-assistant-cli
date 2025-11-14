from typing import Optional, Iterable
from exceptions import AlreadyExistError
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
        return new_contact

    def get(self, name: str) -> Contact | None:
        return self.repo.get(name)

    def add_phone(self, name: str, phone: str) -> bool:
        contact = self.repo.get(name)
        contact.add_phone(Phone(phone))
        self.repo.save(contact)

    def add_contact_or_phone(self, name: str, phone: str) -> str:
        try:
            self.add_contact(name, phone)
            return 'contact'
        except AlreadyExistError:
            self.add_phone(name, phone)
            return 'phone'

    def set_email(self, name: str, raw_email: Optional[str]):
        contact = self.repo.get(name)
        email = None

        if raw_email is not None:
            email = Email(raw_email)

        contact.set_email(email)
        self.repo.save(contact)

    def set_birthday(self, name: str, raw_birthday: Optional[str]):
        contact = self.repo.get(name)
        birthday = None

        if raw_birthday is not None:
            birthday = Birthday(raw_birthday)

        contact.set_birthday(birthday)
        self.repo.save(contact)

    def set_address(self, name: str, raw_address: Optional[str]):
        contact = self.repo.get(name)
        address = None
        if raw_address is not None:
            address = Address(raw_address)

        contact.set_address(address)
        self.repo.save(contact)

    def edit_phone(self, name: str, prev_phone: str, new_phone: str) -> None:
        contact = self.repo.get(name)
        contact.edit_phone(Phone(prev_phone), Phone(new_phone))
        self.repo.save(contact)

    def find(self, search: str) -> Iterable[Contact]:
        return self.repo.find(search)

    def all(self) -> Iterable[Contact]:
        return self.repo.all()

    # TODO: implement other methods to deal with contacts service
