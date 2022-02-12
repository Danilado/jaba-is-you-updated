import io
from pathlib import Path
from threading import Thread
from typing import Final, Dict, Union

import httpx
import pygame
from py7zr import SevenZipFile


class SpriteManager:
    def __init__(self):
        self._images: Dict[str, pygame.surface.Surface] = {}
        self._sprites_folder = Path("sprites/")
        self._thread: Final[Thread] = Thread(target=self._download)
        if not self._sprites_folder.exists():
            self._sprites_folder.mkdir(exist_ok=True)
            self._thread.start()

    def _download(self):
        url = "https://www.dropbox.com/s/1dpe8l37v3jlyfe/sprites.7z?dl=1"
        with httpx.Client(http2=True, http1=False) as client:
            with client.stream("GET",
                               url,
                               follow_redirects=True) as stream:
                file: SevenZipFile  # Pycharm тупой
                with SevenZipFile(io.BytesIO(b"".join(stream.iter_bytes()))) as file:
                    file.extractall(self._sprites_folder)

    def get(self, path: Union[Path, str], alpha: bool = True) -> pygame.Surface:
        if not isinstance(path, Path):
            path = Path(path)
        path = str(path.with_suffix(".webp").resolve())
        if self._thread.is_alive():
            self._thread.join(5)
            if self._thread.is_alive():
                raise RuntimeError("Can't join downlaod thread")
        if path not in self._images:
            if alpha:
                self._images[path] = pygame.image.load(path).convert_alpha()
            else:
                self._images[path] = pygame.image.load(path).convert()
        return self._images[path]
