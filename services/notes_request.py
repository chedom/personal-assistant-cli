from dataclasses import dataclass


@dataclass(frozen=True)
class CreateNoteReq:
    """Request to create a note"""
    title: str
    body: str
    tags: list[str]


@dataclass(frozen=True)
class GetNoteReq:
    """Request to get a note"""
    note_id: int


@dataclass(frozen=True)
class EditTitleReq:
    """Request to edit a note"""
    note_id: int
    title: str


@dataclass(frozen=True)
class EditBodyReq:
    """Request to edit a note"""
    note_id: int
    body: str


@dataclass(frozen=True)
class EditTagsReq:
    """Request to edit a note"""
    note_id: int
    tags: list[str]


@dataclass(frozen=True)
class FindReq:
    """Request to find notes by title"""
    query: str


@dataclass(frozen=True)
class FindByTagsReq:
    """Request to find notes by tags"""
    tags: list[str]


@dataclass(frozen=True)
class SortByTagsReq:
    """Request to sort notes by tags"""
    tags: list[str]


@dataclass(frozen=True)
class DeleteReq:
    """Request to sort notes by tags"""
    note_id: int
