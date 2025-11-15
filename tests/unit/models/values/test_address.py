import unittest

from models.values import Address


class TestAddress(unittest.TestCase):
    """Test Address class"""
    def test_address_creation_success(self):
        """Test that Address is created successfully for valid inputs"""
        test_cases = [
            # Normal valid addresses
            ("Odesa  Deribasivska 10", "Odesa Deribasivska 10"),
            ("Lviv, Shevchenka-street 15", "Lviv, Shevchenka-street 15"),
            ("SomePlace    123", "SomePlace 123"),
            # Test normalization of excessive dots, commas, and spaces
            ("Kyiv.., Khreschatyk,,, 2  .", "Kyiv., Khreschatyk, 2."),
            # Test allowed special characters ('-','/','.')
            ("Dnipro, Naberezhna-Peremohy 20/1", "Dnipro, Naberezhna-Peremohy 20/1"),
            # Cyrillic input
            ("Львів, проспект Свободи 123", "Львів, проспект Свободи 123"),
            # Accepts letters, numbers, spaces, dot, comma, dash and slash
            ("Street 5-2, Apt. 7/3", "Street 5-2, Apt. 7/3"),
            # Trimming & collapsing spaces
            ("    Zhmerynka   33   ", "Zhmerynka 33"),
        ]
        for input_value, expected_value in test_cases:
            with self.subTest(input=input_value, expected=expected_value):
                address = Address(input_value)
                self.assertEqual(address.value, expected_value)

    def test_address_validation_errors(self):
        """Test that Address raises ValueError for invalid inputs"""
        test_cases = [
            # Empty address
            ("", ValueError, "Address should not be empty"),
            ("   ", ValueError, "Address should not be empty"),
            # Too short (< 5 characters)
            ("123", ValueError, "Address is too short"),
            ("Ab 1", ValueError, "Address is too short"),
            # Too long (> 200 characters)
            ("A" * 201, ValueError, "Address is too long"),
            ("Street " + "A" * 195, ValueError, "Address is too long"),
            # No letters
            ("12345", ValueError, "Address must contain letters"),
            ("123 456", ValueError, "Address must contain letters"),
            # No digits (building number)
            ("Street Name", ValueError, "Address must contain a building number"),
            ("Головна Вулиця", ValueError, "Address must contain a building number"),
        ]
        for input_value, expected_exception, expected_message in test_cases:
            with self.subTest(input=input_value, exception=expected_exception.__name__):
                with self.assertRaises(expected_exception) as context:
                    Address(input_value)
                self.assertEqual(str(context.exception), expected_message)
