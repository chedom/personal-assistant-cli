from typing import Protocol


class IDGenerator(Protocol):
    """Generator for the id"""
    def generate(self) -> int: ...
