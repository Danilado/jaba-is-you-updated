from pathlib import Path
from typing import Dict, Union

import pygame

from classes.base_download_manager import BaseDownloadManager
from global_types import SURFACE


class SpriteManager(BaseDownloadManager):
    """Класс необходимый для установки и кеширования спрайтов"""
    path = Path("./sprites/")
    url = "https://www.dropbox.com/s/jpj9b4ghivzj037/sprites1000000.zip?dl=1"

    def __init__(self):
        super().__init__()
        self._images: Dict[str, SURFACE] = {}

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
        if self.thread.is_alive():
            self.thread.join()
        if path not in self._images:
            if alpha:
                self._images[path] = pygame.image.load(path).convert_alpha()
            else:
                self._images[path] = pygame.image.load(path).convert()
        return self._images[path]
