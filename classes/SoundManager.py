import io
import zipfile
from pathlib import Path
from threading import Thread
from typing import Final, Dict, Union

import httpx
import pygame

from global_types import SURFACE


class SoundManager:
    """Класс необходимый для установки и кеширования музыки и звуков"""
    def __init__(self):
        self._sound: Dict[str] = {}
        self._sounds_folder = Path("./sounds/")
        self._thread: Final[Thread] = Thread(target=self._download, daemon=True)

    def start_download(self):
        """Старт скачивания музыки"""
        if not self._sounds_folder.exists() or self._sounds_folder.glob("*"):
            self._sounds_folder.mkdir(exist_ok=True)
            self._thread.start()

    def _download(self):
        """Функция другого потока для скачивания и разархивации музыки и звуков"""
        url = "https://www.dropbox.com/s/krmadrogtl8tq9k/Music.zip?dl=1"
        with httpx.Client(http2=True, http1=False) as client:
            with client.stream("GET",
                               url,
                               follow_redirects=True) as stream:
                with zipfile.ZipFile(io.BytesIO(b"".join(stream.iter_bytes()))) as zip_file:
                    zip_file.extractall(self._sounds_folder)

    def get_music(self, path: Union[Path, str]):
        pygame.mixer.init()
        if not isinstance(path, Path):
            path = Path(path)
        path = str(path.with_suffix(".ogg").resolve())
        if self._thread.is_alive():
            print("b")
            self._thread.join()
        self._sound[path] = pygame.mixer.music.load(path)
        return self._sound[path]
