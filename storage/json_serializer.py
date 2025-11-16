from typing import Generic, TypeVar, Callable
import json

from storage.serializer import Serializer

K = TypeVar("K")
T = TypeVar("T")


class JsonSerializer(Serializer[K, T], Generic[K, T]):
    """JSON-based serializer for storing items."""
    def __init__(
        self,
        to_dict: Callable[[T], dict],
        from_dict: Callable[[dict], T],
        to_key: Callable[[K], str] = lambda k: k,
        from_key: Callable[[str], K] = lambda k: k,
    ):
        self.__to_key: Callable[[K], str] = to_key
        self.__from_key: Callable[[str], K] = from_key
        self.__to_dict: Callable[[T], dict] = to_dict
        self.__from_dict: Callable[[dict], T] = from_dict

    def to_bytes(self, items: dict[K, T]) -> bytes:
        """Serialize items to JSON bytes."""
        payload = {self.__to_key(k): self.__to_dict(v) for k, v in items.items()}
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def from_bytes(self, data: bytes) -> dict[K, T]:
        """Deserialize JSON bytes into a dictionary of items."""
        raw = json.loads(data.decode("utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("JSON root must be an object")

        return {self.__from_key(k): self.__from_dict(v) for k, v in raw.items()}

    def extension(self) -> str | None:
        """Return the file extension for JSON serialization."""
        return 'json'
