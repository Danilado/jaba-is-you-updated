from typing import List, Tuple, Union, Optional, Sequence

import pygame

from elements.global_classes import sprite_manager


class Animation:
    def __init__(self, sprites: Sequence[Optional[Union[pygame.surface.Surface, str]]], sprite_switch_delay: int,
                 position: Tuple[int, int]):
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
        self._timer = pygame.time.get_ticks()

    @property
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
        copy = Animation(self.sprites.copy(), self.sprite_switch_delay, self.position)
        copy._timer = self._timer
        copy.current_sprites_index = self.current_sprites_index
        return copy

    def update(self) -> None:
        if pygame.time.get_ticks() - self._timer >= self.sprite_switch_delay:
            self._timer = pygame.time.get_ticks()
            self.current_sprites_index = (self._current_sprites_index + 1) % len(self.sprites)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.current_sprite, self.position)
