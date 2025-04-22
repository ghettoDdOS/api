import datetime
import os
import uuid
from pathlib import Path
from typing import Any, override

from fastapi import UploadFile
from sqlalchemy import Dialect, types
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.core.config import settings
from app.core.storage import fs_storage


class FSSpecField(types.TypeDecorator):
    impl = types.Unicode
    cache_ok = True

    def __init__(self, *args: Any, upload_to: str | None = None, **kwargs: Any) -> None:
        self._upload_to = upload_to
        super().__init__(*args, **kwargs)

    @property
    def upload_to(self) -> Path:
        return Path(
            datetime.datetime.now(tz=datetime.UTC).strftime(self._upload_to)
            if self._upload_to
            else ""
        )

    def resolve_filename(self, name: str) -> Path:
        base_name = Path(name)
        file_path = self.upload_to / base_name
        if (settings.MEDIA_ROOT / file_path).exists():
            return self.resolve_filename(
                str(f"{base_name.stem}_{uuid.uuid4()}{base_name.suffix}")
            )
        return file_path

    @override
    def process_bind_param(
        self, value: UploadFile | None, dialect: Dialect
    ) -> str | None:
        if not value:
            return None
        filename = self.resolve_filename(value.filename or value.file.name)
        path = settings.MEDIA_ROOT / filename
        with path.open("wb") as output:
            while True:
                chunk = value.file.read(64 * 2**10)
                if not chunk:
                    break
                output.write(chunk)
        return str(filename)

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> str | None:
        return value
