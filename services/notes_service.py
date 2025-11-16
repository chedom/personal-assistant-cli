from typing import Iterable, Optional

from models.note import Note
from models.values import Tag
from repositories.notes_repo import NotesRepository
from services.id_gen import IDGenerator
from services.notes_request import (
    CreateNoteReq,
    GetNoteReq,
    EditTitleReq,
    EditBodyReq,
    EditTagsReq,
    FindReq,
    FindByTagsReq,
    SortByTagsReq,
    DeleteReq,
)


class NotesService:
    """Service for the notes"""
    def __init__(self, repo: NotesRepository, id_gen: IDGenerator):
        """Initialize with a repository and ID generator."""
        self.__repo: NotesRepository = repo
        self.__id_gen: IDGenerator = id_gen

    def add_note(self, req: CreateNoteReq) -> Note:
        """Add a note to the repository"""
        tags = self.__prepare_tags(req.tags)
        note_id = self.__id_gen.generate()
        note = Note(note_id, req.title, req.body, tags)
        self.__repo.add(note)

        return note

    def get_note(self, req: GetNoteReq) -> Optional[Note]:
        """Get a note from the repository"""
        return self.__repo.get(req.note_id)

    def edit_title(self, req: EditTitleReq) -> Note:
        """Edit the title of a note."""
        note = self.__repo.get(req.note_id)
        note.edit_note(new_title=req.title)
        self.__repo.save(note)

        return note

    def edit_body(self, req: EditBodyReq) -> Note:
        """Edit the body of a note."""
        note = self.__repo.get(req.note_id)
        note.edit_note(new_body=req.body)
        self.__repo.save(note)

        return note

    def edit_tags(self, req: EditTagsReq) -> Note:
        """Edit the tags of a note."""
        note = self.__repo.get(req.note_id)
        tags = self.__prepare_tags(req.tags)
        note.edit_note(new_tags=tags)
        self.__repo.save(note)

        return note

    def find(self, req: FindReq) -> Iterable[Note]:
        """Find notes by title"""
        return self.__repo.find(req.query)

    def find_by_tags(self, req: FindByTagsReq) -> Iterable[Note]:
        """Find notes by tags"""
        tags = self.__prepare_tags(req.tags)
        return self.__repo.find_by_tags(tags)

    def sort_by_tags(self, req: SortByTagsReq) -> Iterable[Note]:
        """Sort notes by tags"""
        tags = self.__prepare_tags(req.tags)
        notes = list(self.__repo.all())
        #  Sort notes by tags and updated at (to make it stable)
        notes.sort(
            key=lambda n: (n.count_matching_tags(tags), n.updated_at),
            reverse=True,
        )

        return notes

    def all(self) -> Iterable[Note]:
        """Return all notes."""
        return self.__repo.all()

    def delete_note(self, req: DeleteReq) -> None:
        """Delete a note by ID."""
        note = self.__repo.get(req.note_id)
        self.__repo.delete(note.note_id)

    def __prepare_tags(self, tags: list[str]) -> set[Tag]:
        """Normalize a list of tag strings into a set of Tag objects."""
        return {Tag(t) for t in tags}
