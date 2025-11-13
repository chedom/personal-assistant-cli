from typing import Generic, TypeVar, Callable
import json

T = TypeVar("T")


class JsonSerializer(Generic[T]):
    def __init__(
        self,
        to_dict: Callable[[T], dict],
        from_dict: Callable[dict, [T]],
    ):
        self.__to_dict = to_dict
        self.__from_dict = from_dict

    def to_bytes(self, items: dict[int, T]) -> bytes:
        payload = {k: self.__to_dict(v) for k, v in items.items()}
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def from_bytes(self, data: bytes) -> dict[int, T]:
        raw = json.loads(data.decode("utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("JSON root must be an object")

        return {int(k): self.__from_dict(v) for k, v in raw.items()}
