from repositories.contacts import ContactsRepository
from models.contact import Contact
from models.values import Name, Email, Phone, Address, Birthday


class ContactsService:
    def __init__(self, repo: ContactsRepository):
        self.repo = repo


    def add_contact(self, name : str, phone : str):
        if self.add_phone(name, phone):
            return
        
        new_contact = Contact(name)
        new_contact.add_phone(Phone(phone))

        self.repo.add(new_contact)
        self.repo.save()

    
    def add_phone(self, name : str, phone : str) -> bool:
        existing_contact = self.repo.get(name)
        if existing_contact:
            existing_contact.add_phone(Phone(phone))
            self.repo.save()
            return True
        return False


    def set_email(self, name : str, email : str):
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")
        
        existing_contact.set_email(Email(email))
        self.repo.save()


    def set_birthday(self, name : str, birthday : str):
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")
        
        existing_contact.set_birthday(Birthday(birthday))
        self.repo.save()


    def set_address(self, name : str, address : str):
        existing_contact = self.repo.get(name)
        if not existing_contact:
            raise KeyError(f"User with name {name} does not exist")
        
        existing_contact.set_address(Address(address))
        self.repo.save()
    
    
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

    # TODO: implement other methods to deal with contacts service
