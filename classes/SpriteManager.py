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
        path = str(path.with_suffix(".png").resolve())
        if path not in self._images:
            if alpha:
                self._images[path] = pygame.image.load(path).convert_alpha()
            else:
                self._images[path] = pygame.image.load(path).convert()
        return self._images[path]
