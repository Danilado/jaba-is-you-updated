import abc
from dataclasses import dataclass

from classes.palette_manager import PaletteManager
from classes.sound_manager import SoundManager
from classes.sprite_manager import SpriteManager
from global_types import COLOR


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
    button_color_hover: "COLOR" = (20, 20, 20)


@dataclass
class IuiSettings(AbstractButtonSettings):
    text_size: int = 20
    button_color: "COLOR" = (0, 0, 0)
    button_color_hover: "COLOR" = (20, 20, 20)


sprite_manager = SpriteManager()
sound_manager = SoundManager()
palette_manager = PaletteManager()
