import unittest

from models.values import Phone


class TestPhone(unittest.TestCase):
    """Test Phone class"""
    def test_phone_creation_success(self):
        """Test that Phone is created successfully for valid inputs"""
        test_cases = [
            ("+380671234567", "+380671234567"),
            ("0671234567", "+380671234567"),
            ("380671234567", "+380671234567"),
        ]
        for input_value, expected_value in test_cases:
            with self.subTest(input=input_value, expected=expected_value):
                phone = Phone(input_value)
                self.assertEqual(phone.value, expected_value)

    def test_phone_validation_errors(self):
        """Test that Phone raises ValueError for invalid inputs"""
        test_cases = [
            ("", ValueError, "Phone should not be empty"),
            ("   ", ValueError, "Phone should not be empty"),
            ("671234567", ValueError, "Phone should start with +380"),
            ("+3806712345678", ValueError,
             "Phone must be 13 characters long in format +380XXXXXXXXX"),
            ("1sdfadsd", ValueError, "Phone number can contain only digits"),
        ]
        for input_value, expected_exception, expected_message in test_cases:
            with self.subTest(input=input_value, exception=expected_exception.__name__):
                with self.assertRaises(expected_exception) as context:
                    Phone(input_value)
                self.assertEqual(str(context.exception), expected_message)
