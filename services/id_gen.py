from typing import Protocol


class IDGenerator(Protocol):
    def generate(self) -> id: ...
