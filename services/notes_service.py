from typing import Iterable, Optional
from models.note import Note
from models.values import Tag
from services import (
    IDGenerator,
    CreateNoteReq,
    NotesRepository,
    GetNoteReq,
    EditNoteReq,
    FindReq,
    FindByTagsReq,
    SortByTagsReq,
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
        note = Note(req.title, req.body, tags, note_id=note_id)
        self.__repo.add(note)

        return note

    def get_note(self, req: GetNoteReq) -> Optional[Note]:
        """Get a note from the repository"""
        return self.__repo.get(req.title)

    def edit_note(self, req: EditNoteReq) -> Note:
        """Edit title, body, tags of a note"""
        note = self.__repo.get(req.title)
        tags = self.__prepare_tags(req.tags) if req.tags is not None else None
        note.edit_note(new_title=req.title, new_body=req.body, new_tags=tags)
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
        #  Sort notes by tags and title (to make it stable)
        notes.sort(
            key=lambda n: (n.count_matching_tags(tags), n.title.lower()),
            reverse=True,
        )

        return notes

    def __prepare_tags(self, tags: list[str]) -> set[Tag]:
        return {Tag(t) for t in tags}
