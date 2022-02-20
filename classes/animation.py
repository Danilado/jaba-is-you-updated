from typing import List, Tuple, Union, Optional, Sequence, Dict

import pygame

from elements.global_classes import sprite_manager
from global_types import SURFACE

_sync: Dict[int, int] = {}  # Вот как мне не нравится всё это. ключ - задержка, значение - время


class Animation:
    def __init__(self, sprites: Sequence[Optional[Union[pygame.surface.Surface, str]]], sprite_switch_delay: int,
                 position: Tuple[int, int], synchronize: bool = True):
        if len(sprites) == 0:
            raise ValueError("Sprites are empty")
        self.position: Tuple[int, int] = position
        self.sprites: List[pygame.surface.Surface] = []
        for sprite in sprites:
            if isinstance(sprite, str):
                self.sprites.append(sprite_manager.get(sprite))
            if isinstance(sprite, pygame.surface.Surface):
                self.sprites.append(sprite)
        self.sprite_switch_delay: int = sprite_switch_delay
        self._current_sprites_index: int = 0
        self.synchronize = synchronize
        if synchronize:
            if self.sprite_switch_delay not in _sync:
                _sync[self.sprite_switch_delay] = pygame.time.get_ticks()
            self._timer = _sync[self.sprite_switch_delay]
        else:
            self._timer = pygame.time.get_ticks()

    @property  # Danilado: Не слишком ли длинное имя для property?
    # quswadress: Длинное имя? Извините, в следующий раз буду называть _, csi, или просто i, а вы сами будете додумывать
    # ...для чего этот i нужен. А если серьёзно, то сокращения порой непонятны, я придерживаюсь принципа:
    # ...много букв, зато сразу понятно. Скажи спасибо что я назвал GameStrategy именно так, а не
    # ...AbstractGameGraphicalUserInterfaceStrategy, или же
    # ...абстрактная стратегия игрового графического пользовательского интерфейса.
    def current_sprites_index(self) -> int:
        return self._current_sprites_index

    @current_sprites_index.setter
    def current_sprites_index(self, value: int):
        if value > len(self.sprites):
            raise ValueError("current sprites index should be lower than length of sprites. "
                             "You might want to use `% len(object.sprites)`")
        self._current_sprites_index = value

    @property
    def current_sprite(self) -> pygame.surface.Surface:
        return self.sprites[self.current_sprites_index]

    @current_sprite.setter
    def current_sprite(self, value: pygame.Surface):
        try:
            index = self.sprites.index(value)
        except ValueError:
            raise ValueError("current sprite should be in sprites")
        self.current_sprites_index = index

    def __copy__(self) -> "Animation":
        copy = Animation(self.sprites.copy(), self.sprite_switch_delay, self.position, self.synchronize)
        copy._timer = self._timer
        copy.current_sprites_index = self.current_sprites_index
        return copy

    def update(self) -> None:
        if pygame.time.get_ticks() - self._timer >= self.sprite_switch_delay:
            if self.synchronize:
                _sync[self.sprite_switch_delay] = pygame.time.get_ticks()
                self._timer = _sync[self.sprite_switch_delay]
            else:
                self._timer = pygame.time.get_ticks()
            self.current_sprites_index = (self._current_sprites_index + 1) % len(self.sprites)

    def draw(self, screen: SURFACE) -> None:
        screen.blit(self.current_sprite, self.position)
