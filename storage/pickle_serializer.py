from typing import Generic, TypeVar
import pickle

from storage.serializer import Serializer

K = TypeVar("K")
T = TypeVar("T")


class PickleSerializer(Serializer[K, T], Generic[K, T]):
    """Pickle-based serializer for storing items."""
    def to_bytes(self, items: dict[K, T]) -> bytes:
        """Serialize items to bytes using pickle."""
        return pickle.dumps(items, protocol=pickle.HIGHEST_PROTOCOL)

    def from_bytes(self, data: bytes) -> dict[K, T]:
        """Deserialize bytes into a dictionary of items using pickle."""
        raw = pickle.loads(data)
        if not isinstance(raw, dict):
            raise ValueError("Failed to load resource")

        return raw

    def extension(self) -> str | None:
        """Return the file extension for pickle serialization."""
        return 'pkl'
