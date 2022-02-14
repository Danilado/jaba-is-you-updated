import abc
from dataclasses import dataclass
from typing import Tuple, NewType, Union, TYPE_CHECKING

import pygame

from classes.SpriteManager import SpriteManager


class AbstractButtonSettings(abc.ABC):
    @property
    @abc.abstractmethod
    def text_size(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def button_color(self) -> "COLOR":
        ...

    @property
    @abc.abstractmethod
    def button_color_hover(self) -> "COLOR":
        ...


@dataclass
class GuiSettings(AbstractButtonSettings):
    text_size: int = 20
    button_color: "COLOR" = (93, 0, 255)
    button_color_hover: "COLOR" = (174, 127, 255)


@dataclass
class EuiSettings(AbstractButtonSettings):
    text_size: int = 20
    button_color: "COLOR" = (0, 0, 0)
    button_color_hover: "COLOR" = (10, 10, 10)


@dataclass
class IuiSettings(AbstractButtonSettings):
    text_size: int = 20
    button_color: "COLOR" = (0, 0, 0)
    button_color_hover: "COLOR" = (10, 10, 10)


sprite_manager = SpriteManager()

COLOR = Union[pygame.Color, pygame.color.Color, int, Tuple[int, int, int], Tuple[int, int, int, int]]
