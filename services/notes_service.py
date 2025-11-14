from typing import Iterable, Optional
from models.note import Note
from models.values import Tag

from services.notes_repo import NotesRepository
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
        note = self.__repo.get(req.note_id)
        note.edit_note(new_title=req.title)
        self.__repo.save(note)

        return note

    def edit_body(self, req: EditBodyReq) -> Note:
        note = self.__repo.get(req.note_id)
        note.edit_note(new_body=req.body)
        self.__repo.save(note)

        return note

    def edit_tags(self, req: EditTagsReq) -> Note:
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
        return self.__repo.all()

    def delete_note(self, req: DeleteReq) -> None:
        self.__repo.delete(req.note_id)

    def __prepare_tags(self, tags: list[str]) -> set[Tag]:
        return {Tag(t) for t in tags}
