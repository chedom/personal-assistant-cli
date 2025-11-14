from typing import TypeVar, Generic
from storage.serializer import Serializer
from pathlib import Path

K = TypeVar("K")
T = TypeVar("T")


class FileStorage(Generic[K, T]):
    def __init__(self, filepath: str, serializer: Serializer[K, T]):
        self.__path: Path = Path(filepath)
        self.__serializer: Serializer[T] = serializer

    def load(self) -> dict[K, T]:
        if not self.__path.exists():
            return {}

        data = self.__path.read_bytes()
        return self.__serializer.from_bytes(data)

    # method is not safe, feel free to update
    def save(self, items: dict[K, T]) -> None:
        data = self.__serializer.to_bytes(items)
        with open(self.__path, "wb") as f:
            f.write(data)
