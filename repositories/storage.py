from typing import Protocol, TypeVar


T = TypeVar("T")


class Storage(Protocol[T]):
    def load(self) -> dict[int, T]: ...
    def save(self, notes: dict[int, T]) -> None: ...
