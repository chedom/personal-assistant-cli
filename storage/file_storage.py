from typing import TypeVar, Generic
from pathlib import Path
import os
import tempfile

from storage.serializer import Serializer

K = TypeVar("K")
T = TypeVar("T")

APP_DIR = '.personal-assistant-cli'
HOME_DIR = str(Path.home() / APP_DIR)


class FileStorage(Generic[K, T]):
    """File-based storage for items with serialization."""
    def __init__(self, filename: str, serializer: Serializer[K, T], use_home_dir=True):
        """Initialize the file storage."""
        filepath = f"{filename}.{ext}" if (ext := serializer.extension()) else filename
        if use_home_dir and filepath.startswith('/'):
            raise ValueError("Absolute paths are not allowed when use_home_dir=True")
        if use_home_dir:
            Path(HOME_DIR).mkdir(parents=True, exist_ok=True)
        self.__path: Path = (
            (Path(HOME_DIR) / filepath) if use_home_dir else Path(filepath)
        )
        self.__serializer: Serializer[T] = serializer

    def load(self) -> dict[K, T]:
        """Load items from the storage file."""
        if not self.__path.exists():
            return {}

        data = self.__path.read_bytes()
        return self.__serializer.from_bytes(data)

    def save(self, items: dict[K, T]) -> None:
        """Save items to the storage file."""
        data = self.__serializer.to_bytes(items)

        tmp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                delete=False,
                dir=str(self.__path.parent),
                prefix=Path(self.__path.name).stem + "_", suffix=".tmp"
            ) as tmp:
                tmp_file = Path(tmp.name)
                tmp.write(data)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(tmp_file, self.__path)
        except OSError as e:
            if tmp_file and tmp_file.exists():
                try:
                    tmp_file.unlink()
                except OSError:
                    pass
            raise e
