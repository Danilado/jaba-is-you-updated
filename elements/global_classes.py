from dataclasses import dataclass
from typing import Tuple

from classes.SpriteManager import SpriteManager


@dataclass
class GuiSettings:
    text_size: int = 20
    button_color: Tuple[int, int, int] = (93, 0, 255)
    button_color_hover: Tuple[int, int, int] = (174, 127, 255)


@dataclass
class EuiSettings:
    text_size: int = 20
    button_color: Tuple[int, int, int] = (0, 0, 0)
    button_color_hover: Tuple[int, int, int] = (10, 10, 10)


@dataclass
class IuiSettings:
    text_size: int = 20
    button_color: Tuple[int, int, int] = (0, 0, 0)
    button_color_hover: Tuple[int, int, int] = (10, 10, 10)


sprite_manager = SpriteManager()
