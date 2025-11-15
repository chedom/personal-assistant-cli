import unittest
from datetime import datetime as DateTime

from models.note import Note
from models.values import Tag


class TestNote(unittest.TestCase):
    """Test Note class"""
    def setUp(self):
        self.today_date = DateTime.now().date()
        self.note = Note(1, title="Test Note",
                         body="This is a test note",
                         tags=set([Tag("test tag"), Tag("tag2")]))

    def test_note_init(self):
        """Test note initialization"""
        self.assertEqual(self.note.note_id, 1)
        self.assertEqual(self.note.updated_at.date(), self.today_date)
        self.assertEqual(self.note.title.value, "Test Note")
        self.assertEqual(self.note.body.value, "This is a test note")
        self.assertEqual(self.note.tags, set([Tag("test tag"), Tag("tag2")]))

    def test_note_contains(self):
        """Test note contains"""
        self.assertTrue(self.note.contains("Test Note"))
        self.assertTrue(self.note.contains("test note"))
        self.assertTrue(self.note.contains("this is"))
        self.assertFalse(self.note.contains("not a test note"))

    def test_note_count_matching_tags(self):
        """Test note count matching tags"""
        self.assertEqual(self.note.count_matching_tags(
            set([Tag("test tag")])), 1)
        self.assertEqual(self.note.count_matching_tags(
            set([Tag("not a test tag")])), 0)
        self.assertEqual(self.note.count_matching_tags(
            set([Tag("not a test tag"), Tag("tag2")])), 1)
        self.assertEqual(self.note.count_matching_tags(
            set([Tag("test tag"), Tag("tag2")])), 2)

    def test_note_to_dict(self):
        """Test note to dictionary"""
        self.assertEqual(self.note.to_dict(), {
            "title": "Test Note",
            "body": "This is a test note",
            "tags": ["tag2", "test-tag"],
            "note_id": 1,
            "created_at": self.note.created_at.isoformat(),
            "updated_at": self.note.updated_at.isoformat()
        })

    def test_note_from_dict(self):
        """Test note from dictionary"""
        data = {
            "title": "Test Note",
            "body": "This is a test note",
            "tags": ["tag2", "test-tag"],
            "note_id": 1,
            "created_at": self.note.created_at.isoformat(),
            "updated_at": self.note.updated_at.isoformat()
        }
        note = Note.from_dict(data)
        self.assertEqual(note.title.value, "Test Note")
        self.assertEqual(note.body.value, "This is a test note")
        self.assertEqual(note.tags, set([Tag("tag2"), Tag("test-tag")]))
        self.assertEqual(note.note_id, 1)
        self.assertEqual(note.created_at, self.note.created_at)
        self.assertEqual(note.updated_at, self.note.updated_at)

    def test_note_edit_note(self):
        """Test note edit note"""
        self.note.edit_note(new_title="New Title", new_body="New Body",
                            new_tags=set([Tag("new tag")]))
        self.assertEqual(self.note.title.value, "New Title")
        self.assertEqual(self.note.body.value, "New Body")
        self.assertEqual(self.note.tags, set([Tag("new tag")]))
