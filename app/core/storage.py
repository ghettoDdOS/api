import shutil
from pathlib import Path
from typing import BinaryIO, List

from app.core.config import settings

DEFAULT_CHUNK_SIZE = 64 * 2**10


class FileSystemStorage:
    def __init__(
        self,
        *,
        location: Path,
        base_url: str,
    ) -> None:
        self.location = location.absolute()
        self.base_url = base_url

    def path(self, name: str) -> Path:
        return self.location / name

    def url(self, name: str) -> str:
        return f"{self.base_url}/{name}"

    def save(self, name: str, content: BinaryIO) -> None:
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as output:
            content.seek(0)
            while True:
                chunk = content.read(DEFAULT_CHUNK_SIZE)
                if not chunk:
                    break
                output.write(chunk)

    def open(self, name: str) -> BinaryIO:
        with self.path(name).open("rb") as content:
            return content

    def delete(self, name: str) -> None:
        shutil.rmtree(self.path(name))


fs_storage = FileSystemStorage(
    location=settings.MEDIA_ROOT,
    base_url=settings.MEDIA_URL,
)
