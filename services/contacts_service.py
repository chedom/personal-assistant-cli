from typing import Optional, Iterable
from datetime import datetime, date, timedelta

from exceptions import AlreadyExistError
from repositories.contacts_repo import ContactsRepository
from models import Contact
from models.values import Email, Phone, Address, Birthday


class ContactsService:
    """Service layer for managing contacts."""
    def __init__(self, repo: ContactsRepository):
        """Initialize the ContactsService with a repository."""
        self.repo = repo

    def add_contact(self, name: str, phone: str) -> Contact:
        """Add a new contact with one phone."""
        new_contact = Contact(name)
        new_contact.add_phone(Phone(phone))

        self.repo.add(new_contact)
        return new_contact

    def get(self, name: str) -> Contact | None:
        """Get a contact by name."""
        return self.repo.get(name)

    def add_phone(self, name: str, phone: str) -> bool:
        """Add a phone to an existing contact."""
        contact = self.repo.get(name)
        contact.add_phone(Phone(phone))
        self.repo.save(contact)

    def add_contact_or_phone(self, name: str, phone: str) -> str:
        """Add contact or phone if contact exists. Returns 'contact' or 'phone'."""
        try:
            self.add_contact(name, phone)
            return 'contact'
        except AlreadyExistError:
            self.add_phone(name, phone)
            return 'phone'

    def set_email(self, name: str, raw_email: Optional[str]):
        """Set or remove email for a contact."""
        contact = self.repo.get(name)
        email = None

        if raw_email is not None:
            email = Email(raw_email)

        contact.set_email(email)
        self.repo.save(contact)

    def set_birthday(self, name: str, raw_birthday: Optional[str]):
        """Set or remove birthday for a contact."""
        contact = self.repo.get(name)
        birthday = None

        if raw_birthday is not None:
            birthday = Birthday(raw_birthday)

        contact.set_birthday(birthday)
        self.repo.save(contact)

    def set_address(self, name: str, raw_address: Optional[str]):
        """Set or remove address for a contact."""
        contact = self.repo.get(name)
        address = None
        if raw_address is not None:
            address = Address(raw_address)

        contact.set_address(address)
        self.repo.save(contact)

    def edit_phone(self, name: str, prev_phone: str, new_phone: str) -> None:
        """Replace an existing phone with a new one."""
        contact = self.repo.get(name)
        contact.edit_phone(Phone(prev_phone), Phone(new_phone))
        self.repo.save(contact)

    def del_phone(self, name: str, phone: str) -> bool:
        """Delete a phone from a contact. Returns True if deleted."""
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")

        phone_to_delete = Phone(phone)
        if existing_contact.del_phone(phone_to_delete):
            return True
        else:
            return False

    def del_contact(self, name: str):
        """Delete a contact by name."""
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")

        self.repo.delete(name)

    def find(self, search: str) -> Iterable[Contact]:
        """Search contacts by string."""
        return self.repo.find(search)

    def all(self) -> Iterable[Contact]:
        """Return all contacts."""
        return self.repo.all()

    def upcoming_birthdays(
            self, num_days: int) -> Iterable[tuple[Contact, date]]:
        """Return contacts with birthdays in the next num_days."""
        contacts = self.all()
        today = date.today()
        limit_day = today + timedelta(days=num_days)

        result = []

        for contact in contacts:
            if contact.birthday is None:
                continue

            try:
                bday = datetime.strptime(
                    contact.birthday.value, "%d.%m.%Y").date()
            except ValueError:
                continue

            # Find nearest birthday
            try:
                birthday_this_year = date(today.year, bday.month, bday.day)
            except ValueError:  # 29 Feb in short year
                # 28 Feb for short year
                birthday_this_year = date(today.year, bday.month, bday.day - 1)

            if birthday_this_year < today:
                try:
                    next_birthday = date(today.year + 1, bday.month, bday.day)
                except ValueError:  # 29 Feb in short year
                    # 28 Feb for short year
                    next_birthday = date(
                        today.year + 1, bday.month, bday.day - 1)
            else:
                next_birthday = birthday_this_year

            if today <= next_birthday <= limit_day:
                result.append((contact, next_birthday))

        result.sort(key=lambda item: item[1])

        return result
