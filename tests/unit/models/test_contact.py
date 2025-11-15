import unittest

from exceptions import AlreadyExistError, NotFoundError
from models.contact import Contact
from models.values import Phone, Email, Birthday, Address


class TestContact(unittest.TestCase):
    def setUp(self):
        self.contact = Contact(name="John Doe", phones=[Phone("+380671234567")])

    def test_contact_init(self):
        """Test Contact object initialization"""
        contact = Contact(name="Jane Doe", phones=[Phone("+380631234567")])
        self.assertEqual(contact.name.value, "Jane Doe")
        self.assertEqual(len(contact.phones), 1)
        self.assertEqual(contact.phones[0].value, "+380631234567")

    def test_contact_str(self):
        """Test __str__ method returns a string representation"""
        result = str(self.contact)
        self.assertIsInstance(result, str)
        self.assertIn("John Doe", result)
        self.assertIn("+380671234567", result)

    def test_add_phone(self):
        """Test add_phone method adds a phone number"""
        new_phone = Phone("+380931234567")
        self.contact.add_phone(new_phone)
        self.assertEqual(len(self.contact.phones), 2)
        self.assertEqual(self.contact.phones[1].value, "+380931234567")

    def test_add_phone_raises_already_exist_error(self):
        """Test add_phone raises AlreadyExistError when phone already exists"""
        duplicate_phone = Phone("+380671234567")  # Same as in setUp
        with self.assertRaises(AlreadyExistError) as context:
            self.contact.add_phone(duplicate_phone)
        self.assertIn("Phone", str(context.exception))
        self.assertEqual(len(self.contact.phones), 1)  # Phone not added

    def test_edit_email(self):
        """Test edit_email method changes the email"""
        new_email = Email("newmail@example.com")
        self.contact.set_email(new_email)
        self.assertEqual(self.contact.email.value, "newmail@example.com")

    def test_remove_email(self):
        """Test removing the email sets it to None or handles removal"""
        new_email = Email("johndoe@example.com")
        self.contact.set_email(new_email)
        self.assertEqual(self.contact.email.value, "johndoe@example.com")
        self.contact.set_email(None)
        self.assertIsNone(self.contact.email)

    def test_set_invalid_email(self):
        """Test setting an invalid email raises ValueError"""
        with self.assertRaises(ValueError):
            self.contact.set_email(Email("not-an-email"))

    def test_edit_phone(self):
        """Test edit_phone method changes a phone number"""
        prev_phone = Phone("+380671234567")
        new_phone = Phone("+380931234567")
        self.contact.edit_phone(prev_phone, new_phone)
        self.assertEqual(len(self.contact.phones), 1)
        self.assertEqual(self.contact.phones[0].value, "+380931234567")

    def test_edit_phone_raises_not_found_error(self):
        """Test edit_phone raises NotFoundError when previous phone doesn't exist"""
        non_existent_phone = Phone("+380999999999")
        new_phone = Phone("+380931234567")
        with self.assertRaises(NotFoundError) as context:
            self.contact.edit_phone(non_existent_phone, new_phone)
        self.assertIn("Phone", str(context.exception))
        self.assertEqual(len(self.contact.phones), 1)  # Phone not changed

    def test_edit_phone_raises_already_exist_error(self):
        """Test edit_phone raises AlreadyExistError when new phone already exists"""
        prev_phone = Phone("+380671234567")
        # Try to edit to the same phone number (already exists)
        with self.assertRaises(AlreadyExistError) as context:
            self.contact.edit_phone(prev_phone, prev_phone)
        self.assertIn("Phone", str(context.exception))

    def test_edit_phone_raises_already_exist_error_for_other_phone(self):
        """Test edit_phone raises AlreadyExistError when new phone exists in list"""
        # Add a second phone
        second_phone = Phone("+380931234567")
        self.contact.add_phone(second_phone)

        # Try to edit first phone to match second phone
        prev_phone = Phone("+380671234567")
        with self.assertRaises(AlreadyExistError) as context:
            self.contact.edit_phone(prev_phone, second_phone)
        self.assertIn("Phone", str(context.exception))
        self.assertEqual(len(self.contact.phones), 2)  # Phones unchanged

    def test_set_birthday(self):
        """Test setting a birthday"""
        birthday_date = Birthday("01.01.2000")
        self.contact.set_birthday(birthday_date)
        self.assertIsNotNone(self.contact.birthday)
        self.assertEqual(self.contact.birthday.value, birthday_date.value)

    def test_edit_birthday(self):
        """Test editing birthday after setting it"""
        birthday1 = Birthday("01.01.2000")
        birthday2 = Birthday("02.11.2000")
        self.contact.set_birthday(birthday1)
        self.assertEqual(self.contact.birthday.value, birthday1.value)
        self.contact.set_birthday(birthday2)
        self.assertEqual(self.contact.birthday.value, birthday2.value)

    def test_remove_birthday(self):
        """Test removing the birthday sets it to None or handles removal"""
        bday = Birthday("03.03.1977")
        self.contact.set_birthday(bday)
        self.assertEqual(self.contact.birthday.value, bday.value)
        self.contact.set_birthday(None)
        self.assertIsNone(self.contact.birthday)

    def test_set_address(self):
        """Test setting an address"""
        address = Address("123 Main St, Anytown, USA")
        self.contact.set_address(address)
        self.assertEqual(self.contact.address.value, address.value)

    def test_to_dict(self):
        """Test to_dict returns dictionary representation"""
        result = self.contact.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertEqual(result["name"], "John Doe")
        self.assertIn("phones", result)
        self.assertEqual(len(result["phones"]), 1)
        self.assertEqual(result["phones"][0], "+380671234567")

        if self.contact.email:
            self.assertEqual(result["email"], self.contact.email.value)
        if self.contact.birthday:
            self.assertTrue("birthday" in result)
        if self.contact.address:
            self.assertEqual(result["address"], self.contact.address.value)

    def test_from_dict(self):
        """Test from_dict creates a Contact from dictionary"""
        data = {
            "name": "Bob Miller",
            "email": "bob@example.com",
            "phones": ["+380501112233"],
            "birthday": "01-12-1990",
            "address": "123 Main St, Anytown, USA"
        }
        contact = Contact.from_dict(data)
        self.assertEqual(contact.name.value, "Bob Miller")
        self.assertEqual(contact.email.value, "bob@example.com")
        self.assertEqual(len(contact.phones), 1)
        self.assertEqual(contact.phones[0].value, "+380501112233")
        self.assertEqual(contact.birthday.value, "01.12.1990")
        self.assertEqual(contact.address.value, "123 Main St, Anytown, USA")

    def test_remove_address(self):
        """Test removing the address sets it to None or handles removal"""
        address = Address("123 Main St, Anytown, USA")
        self.contact.set_address(address)
        self.assertEqual(self.contact.address.value, address.value)
        self.contact.set_address(None)
        self.assertIsNone(self.contact.address)

    def test_add_phones(self):
        """Test add_phones method adds multiple phone numbers"""
        new_phones = [Phone("+380931234567"), Phone("+380501112233")]
        self.contact.add_phones(new_phones)
        self.assertEqual(len(self.contact.phones), 3)
        self.assertEqual(self.contact.phones[1].value, "+380931234567")
        self.assertEqual(self.contact.phones[2].value, "+380501112233")
