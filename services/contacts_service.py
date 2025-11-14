from typing import Optional, Iterable
from exceptions import AlreadyExistError
from repositories.contacts import ContactsRepository
from models import Contact
from models.values import Email, Phone, Address, Birthday
from datetime import datetime, date, timedelta


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

    def del_phone(self, name: str, phone: str) -> bool:
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")

        phone_to_delete = Phone(phone)
        if existing_contact.del_phone(phone_to_delete):
            self.repo.save()
            return True
        else:
            return False

    def del_contact(self, name: str):
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")

        self.repo.delete(name)
        self.repo.save()

    def find(self, search: str) -> Iterable[Contact]:
        return self.repo.find(search)

    def all(self) -> Iterable[Contact]:
        return self.repo.all()

    def upcomming_birthdays(
            self, num_days: int) -> Iterable[tuple[Contact, date]]:
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

    # TODO: implement other methods to deal with contacts service
