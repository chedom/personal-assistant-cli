from dataclasses import dataclass
from optparse import Option
from typing import Sequence, Optional


@dataclass(frozen=True)
class CreateNoteReq:
    """Request to create a note"""
    title: str
    body: str
    tags: Sequence[str] = ()


@dataclass(frozen=True)
class GetNoteReq:
    """Request to get a note"""
    title: str


@dataclass(frozen=True)
class EditNoteReq:
    """Request to edit a note"""
    note_id: int
    title: Optional[str]
    body: Optional[str]
    tags: Optional[Sequence[str]]

@dataclass(frozen=True)
class FindReq:
    """Request to find notes by title"""
    query: str

@dataclass(frozen=True)
class FindByTagsReq:
    """Request to find notes by tags"""
    tags: Sequence[str] = ()


@dataclass(frozen=True)
class SortByTagsReq:
    """Request to sort notes by tags"""
    tags: Sequence[str] = ()
