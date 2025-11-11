from dataclasses import dataclass
from typing import Iterable, Sequence, Optional
from models.note import Note
from models.values import Tag
from repositories.notes import NotesRepository


@dataclass(frozen=True)
class CreateNoteReq:
    """Request to create a note"""
    title: str
    body: str = ""
    tags: Sequence[str] = ()


@dataclass(frozen=True)
class GetNoteReq:
    """Request to get a note"""
    title: str


@dataclass
class EditNoteReq:
    """Request to edit a note"""
    title: str
    new_body: str


@dataclass
class EditTagsReq:
    """Request to edit the tags of a note"""
    title: str
    tags: Sequence[str] = ()


@dataclass
class FindByTitleReq:
    """Request to find notes by title"""
    query: str

@dataclass
class FindByTagsReq:
    """Request to find notes by tags"""
    tags: Sequence[str] = ()


@dataclass
class SortByTagsReq:
    """Request to sort notes by tags"""
    tags: Sequence[str] = ()


class NotesService:
    """Service for the notes"""
    def __init__(self, repo: NotesRepository):
        self.repo = repo

    def add_note(self, req: CreateNoteReq) -> Note:
        """Add a note to the repository"""
        tags = {Tag(t) for t in req.tags}
        note = Note(req.title, req.body, tags)
        self.repo.add(note)

        return note

    def get_note(self, req: GetNoteReq) -> Optional[Note]:
        """Get a note from the repository"""
        return self.repo.get(req.title)

    def edit_tags(self, req: EditTagsReq) -> Note:
        """Edit the tags of a note"""
        note = self.repo.get(req.title)
        note.edit_tags(req.tags)
        self.repo.save(note)

        return note

    def find_by_title(self, req: FindByTitleReq) -> Iterable[Note]:
        """Find notes by title"""
        return self.repo.find_by_title(req.query)

    def find_by_tags(self, req: FindByTagsReq) -> Iterable[Note]:
        """Find notes by tags"""
        return self.repo.find_by_tags(req.tags)

    def sort_by_tags(self, req: SortByTagsReq) -> Iterable[Note]:
        """Sort notes by tags"""
        tags = {Tag(t) for t in req.tags}
        notes = list(self.repo.all())
        #  Sort notes by tags and title (to make it stable)
        notes.sort(key=lambda n: (len(n.tags & tags), n.title.lower()),
                   reverse=True)

        return notes
