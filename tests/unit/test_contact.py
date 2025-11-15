import unittest

from exceptions import AlreadyExistError, NotFoundError
from models.contact import Contact
from models.values import Phone, Email


class TestContact(unittest.TestCase):
    def setUp(self):
        # Basic Contact creation, adjust fields as required by your model
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

    def test_to_dict(self):
        """Test to_dict returns dictionary representation"""
        result = self.contact.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertEqual(result["name"], "John Doe")
        self.assertIn("phones", result)
        self.assertEqual(len(result["phones"]), 1)
        self.assertEqual(result["phones"][0], "+380671234567")

    def test_from_dict(self):
        """Test from_dict creates a Contact from dictionary"""
        data = {
            "name": "Bob Miller",
            "email": "bob@example.com",
            "phones": ["+380501112233"],
            "birthday": None,
            "address": None
        }
        contact = Contact.from_dict(data)
        self.assertEqual(contact.name.value, "Bob Miller")
        self.assertEqual(contact.email.value, "bob@example.com")
        self.assertEqual(len(contact.phones), 1)
        self.assertEqual(contact.phones[0].value, "+380501112233")

    def test_add_phones(self):
        """Test add_phones method adds multiple phone numbers"""
        new_phones = [Phone("+380931234567"), Phone("+380501112233")]
        self.contact.add_phones(new_phones)
        self.assertEqual(len(self.contact.phones), 3)
        self.assertEqual(self.contact.phones[1].value, "+380931234567")
        self.assertEqual(self.contact.phones[2].value, "+380501112233")
