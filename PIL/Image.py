from __future__ import annotations

import base64
import imghdr
from typing import Any

_MIN_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
)


class ImageFile:
    def __init__(self, data: bytes | None = None, mode: str = "RGB", size: tuple[int, int] = (1, 1), format: str = "PNG") -> None:
        self._data = data or _MIN_PNG
        self.mode = mode
        self.size = size
        self.format = format

    def verify(self) -> None:  # pragma: no cover - compatibility shim
        return None

    def convert(self, mode: str) -> "ImageFile":
        self.mode = mode
        return self

    def thumbnail(self, size: tuple[int, int]) -> None:  # pragma: no cover - no-op
        return None

    def save(self, fp: Any, format: str = "PNG", quality: int = 90) -> None:  # noqa: ARG002
        data = self._data or _MIN_PNG
        self.format = format
        if hasattr(fp, "write"):
            fp.write(data)
        else:
            with open(fp, "wb") as handle:  # pragma: no cover
                handle.write(data)


def open(file_obj: Any) -> ImageFile:
    data = file_obj.read()
    file_obj.seek(0)
    kind = imghdr.what(None, data)
    fmt = (kind or "png").upper()
    return ImageFile(data=data, format=fmt)


def new(mode: str, size: tuple[int, int], color: str | tuple[int, int, int] = "white") -> ImageFile:  # noqa: ARG001
    return ImageFile(mode=mode, size=size)
