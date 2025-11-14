from typing import Optional
from exceptions import AlreadyExistError, NotFoundError
from models.values import Name, Email, Phone, Address, Birthday
import re


class Contact:
    def __init__(self, name: str):
        self.name = Name(name)
        self.email: Optional[Email] = None
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None

    def set_email(self, email: Email):
        self.email = email

    def add_phone(self, phone: Phone):
        if self.__phone_exists(phone):
            raise AlreadyExistError("Phone")

        self.phones.append(phone)

    def edit_phone(self, prev_phone: Phone, new_phone: Phone):
        if not self.__phone_exists(prev_phone):
            raise NotFoundError(f"Phone {prev_phone}")
        if self.__phone_exists(new_phone):
            raise AlreadyExistError("Phone")

        for i, p in enumerate(self.phones):
            if p == prev_phone:
                self.phones[i] = new_phone
                break

    def __phone_exists(self, phone: Phone) -> bool:
        return any(p == phone for p in self.phones)

    def add_phones(self, phones: list[Phone]):
        for phone in phones:
            self.add_phone(phone)

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def set_address(self, address: Address):
        self.address = address

    def is_matching(self, search: str) -> bool:
        search_values = [self.name.value]
        search_values.extend(str(phone) for phone in self.phones)

        if self.email:
            search_values.append(self.email.value)
        if self.address:
            search_values.append(self.address.value)
        if self.birthday:
            search_values.append(self.birthday.value)

        search_lower = search.casefold()

        # Perform regex search
        if "*" in search:
            regex_pattern = re.escape(search_lower).replace(r'\*', '.*')
            regex_pattern = f"^{regex_pattern}$"
            return any(re.match(regex_pattern, val.casefold()) is not None for val in search_values)

        # Perform exact search
        return any(search_lower == val.casefold() for val in search_values)

    def __str__(self) -> str:
        phones_str = "| ".join(p.value for p in self.phones) or "—"
        parts = [f"Contact: {self.name.value}", f"phones: {phones_str}"]

        if self.email:
            parts.append(f"email: {self.email}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        if self.address:
            parts.append(f"address: {self.address}")

        return ", ".join(parts)
