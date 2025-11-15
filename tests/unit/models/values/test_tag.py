import unittest

from models.values import Tag


class TestTag(unittest.TestCase):
    """Test Tag class"""
    def test_tag_creation_success(self):
        """Test that Tag is created successfully for valid inputs"""
        test_cases = [
            ("work", "work"),
            ("my work", "my-work"),
            ("my-work", "my-work"),
            ("my_work", "mywork"),
            ("my work 123", "my-work-123"),
            ("  work  ", "work"),
            (" My Work QQ", "my-work-qq")
        ]
        for input_value, expected_value in test_cases:
            with self.subTest(input=input_value, expected=expected_value):  
                tag = Tag(input_value)
                self.assertEqual(tag.value, expected_value)

    def test_tag_validation_errors(self):
        """Test that Tag raises ValueError for invalid inputs"""
        test_cases = [
            ("", ValueError, "Tag couldn't be empty"),
        ]
        for input_value, expected_exception, expected_message in test_cases:
            with self.subTest(input=input_value, exception=expected_exception.__name__):
                with self.assertRaises(expected_exception) as context:
                    Tag(input_value)
                self.assertEqual(str(context.exception), expected_message)
