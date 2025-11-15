import unittest

from models.values import Email


class TestEmail(unittest.TestCase):
    """Test Email class"""
    def test_email_creation_success(self):
        """Test that Email is created successfully for valid inputs"""
        test_cases = [
            ("test@example.com", "test@example.com"),
            ("test+user@example.com", "test+user@example.com"),
            ("test@example.com.ua", "test@example.com.ua"),
        ]
        for input_value, expected_value in test_cases:
            with self.subTest(input=input_value, expected=expected_value):
                email = Email(input_value)
                self.assertEqual(email.value, expected_value)

    def test_email_validation_errors(self):
        """Test that Email raises ValueError for invalid inputs"""
        test_cases = [
            ("", ValueError, "Email should not be empty"),
            ("   ", ValueError, "Email should not be empty"),
            ("test@example", ValueError, "Invalid email format"),
            ("@example.com", ValueError, "Invalid email format"),
        ]
        for input_value, expected_exception, expected_message in test_cases:
            with self.subTest(input=input_value, exception=expected_exception.__name__):
                with self.assertRaises(expected_exception) as context:
                    Email(input_value)
                self.assertEqual(str(context.exception), expected_message)
