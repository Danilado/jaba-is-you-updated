import io
import zipfile
from pathlib import Path
from threading import Thread
from typing import Final, Dict, Union

import httpx
import pygame

from global_types import SURFACE


class SpriteManager:
    """Класс необходимый для установки и кеширования спрайтов"""

    def __init__(self):
        self._images: Dict[str, SURFACE] = {}
        self._sprites_folder = Path("./sprites/")
        self._thread: Final[Thread] = Thread(
            target=self._download, daemon=True)

    def start_download(self):
        """Старт скачивания спрайтов"""
        if not self._sprites_folder.exists() or self._sprites_folder.glob("*"):
            self._sprites_folder.mkdir(exist_ok=True)
            self._thread.start()

    def _download(self):
        """Функция другого потока для скачивания и разархивации спрайтов"""
        url = "https://www.dropbox.com/s/8wpc6a8ppvl3fjk/sprites321.zip?dl=1"
        with httpx.Client(http2=True, http1=False) as client:
            with client.stream("GET",
                               url,
                               follow_redirects=True) as stream:
                with zipfile.ZipFile(io.BytesIO(b"".join(stream.iter_bytes()))) as zip_file:
                    zip_file.extractall(self._sprites_folder)

    def get(self, path: Union[Path, str], alpha: bool = True) -> SURFACE:
        """
        Функция для получения спрайта из кэша. Если в кэше нету нужного спрайта, он загрузится и
        сконвертируется используя параметр `alpha`.

        :param path: Путь до спрайта, например sprites/jaba/b00
        :param alpha: Если этот параметр установлен, и спрайт не в кэше, будет происходить convert_alpha вместо convert
        :return: Загруженный спрайт через pygame.image.load
        """
        if not isinstance(path, Path):
            path = Path(path)
        path = str(path.with_suffix(".webp").resolve())
        if self._thread.is_alive():
            print("a")
            self._thread.join(5)
            if self._thread.is_alive():
                raise RuntimeError("Can't join downlaod thread")
        if path not in self._images:
            if alpha:
                self._images[path] = pygame.image.load(path).convert_alpha()
            else:
                self._images[path] = pygame.image.load(path).convert()
        return self._images[path]
