from typing import Protocol, TypeVar

K = TypeVar("K")
T = TypeVar("T")


class Storage(Protocol[K, T]):
    def load(self) -> dict[K, T]: ...
    def save(self, notes: dict[K, T]) -> None: ...
