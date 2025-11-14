from typing import Protocol, TypeVar

K = TypeVar("K")
T = TypeVar("T")


class Serializer(Protocol[K, T]):
    def to_bytes(self, items: dict[K, T]) -> bytes: ...
    def from_bytes(self, data: bytes) -> dict[K, T]: ...
    def extension(self) -> str | None: ...
