from typing import Protocol, TypeVar

T = TypeVar("T")


class Serializer(Protocol[T]):
    def to_bytes(self, items: dict[int, T]) -> bytes: ...
    def from_bytes(self, data: bytes) -> dict[int, T]: ...
