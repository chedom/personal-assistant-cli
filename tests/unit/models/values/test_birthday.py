import unittest

from models.values import Birthday


class TestBirthday(unittest.TestCase):
    """Test Birthday class"""
    def test_birthday_creation_success(self):
        """Test that Birthday is created successfully for valid inputs"""
        test_cases = [
            ("01.01.2000", "01.01.2000"),
            ("01/01/2000", "01.01.2000"),
            ("01-01-2000", "01.01.2000"),
            # 29-th February in leap year
            ("29-02-2024", "29.02.2024"),
        ]
        for input_value, expected_value in test_cases:
            with self.subTest(input=input_value, expected=expected_value):
                birthday = Birthday(input_value)
                self.assertEqual(birthday.value, expected_value)

    def test_birthday_validation_errors(self):
        """Test that Birthday raises ValueError for invalid inputs"""
        test_cases = [
            ("", ValueError, "Birthday should not be empty"),
            ("   ", ValueError, "Birthday should not be empty"),
            ("32.01.2000", ValueError, "Day must be between 01 and 31"),
            ("01.13.2000", ValueError, "Month must be between 01 and 12"),
            ("01.01.0000", ValueError, "Invalid calendar date"),
            # 29-th February in short year
            ("29.02.2023", ValueError, "Invalid calendar date"),
            ("01.01.2050", ValueError, "Birthday cannot be in the future"),
        ]
        for input_value, expected_exception, expected_message in test_cases:
            with self.subTest(input=input_value, exception=expected_exception.__name__):
                with self.assertRaises(expected_exception) as context:
                    Birthday(input_value)
                self.assertEqual(str(context.exception), expected_message)
