from typing import Optional
from models.values import Name, Email, Phone, Address, Birthday


class Contact:
    def __init__(self, name : str):
        self.name = Name(name)
        self.email: Optional[Email] = None
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None


    def set_email(self, email : Email):
        self.email = email


    def add_phone(self, phone : Phone):
        for phone_number in self.phones:
            if phone_number == phone:
                return
            
        self.phones.append(phone)


    def add_phones(self, phones : list[Phone]):
        for phone in phones:
            self.add_phone(phone)

    
    def set_birthday(self, birthday : Birthday):
        self.birthday = birthday


    def set_address(self, address : Address):
        self.address = address


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
    
    
    def del_phone(self, phone: Phone):
        for i, phone_number in enumerate(self.phones):
            if phone_number == phone:
                del self.phones[i]
                return True
        return False
    