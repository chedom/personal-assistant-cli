import re
from typing import Optional, Self
from exceptions import AlreadyExistError, NotFoundError
from models.values import Name, Email, Phone, Address, Birthday


class Contact:
    def __init__(
        self, name: str,
        email: Optional[Email] = None,
        phones: list[Phone] = None,
        birthday: Optional[Birthday] = None,
        address: Optional[Address] = None,
    ):
        self.name: Name = Name(name)
        self.email: Optional[Email] = email
        self.phones: list[Phone] = phones or []
        self.birthday: Optional[Birthday] = birthday
        self.address: Optional[Address] = address

    def set_email(self, email: Email):
        """Set the email"""
        self.email = email

    def add_phone(self, phone: Phone):
        """Add a phone"""
        if self.__phone_exists(phone):
            raise AlreadyExistError("Phone")

        self.phones.append(phone)

    def edit_phone(self, prev_phone: Phone, new_phone: Phone):
        """Edit a phone"""
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
        """Add multiple phones"""
        for phone in phones:
            self.add_phone(phone)

    def set_birthday(self, birthday: Birthday):
        """Set the birthday"""
        self.birthday = birthday

    def set_address(self, address: Address):
        """Set the address"""
        self.address = address

    def is_matching(self, search: str) -> bool:
        """Check if the contact matches the search"""
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
            return any(
                re.match(regex_pattern, val.casefold()) is not None
                for val in search_values
            )

        # Perform exact search
        return any(search_lower == val.casefold() for val in search_values)

    def del_phone(self, phone: Phone):
        for i, phone_number in enumerate(self.phones):
            if phone_number == phone:
                del self.phones[i]
                return True
        return False

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

    def to_dict(self) -> dict:
        """Convert the contact to a dictionary"""
        return {
            "name": self.name.value,
            "email": self.email.value if self.email else None,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value if self.birthday else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Convert the dictionary to a contact"""
        return cls(
            name=data["name"],
            email=Email(data["email"]) if data["email"] else None,
            phones=[Phone(p) for p in data["phones"]],
            birthday=Birthday(data["birthday"]) if data["birthday"] else None,
            address=Address(data["address"]) if data["address"] else None,
        )
