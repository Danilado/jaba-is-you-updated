import os

import pygame

from classes.animation import Animation
from classes.button import Button
from elements.global_classes import sprite_manager
from settings import TEXT_ONLY


class ObjectButton(Button):
    def __init__(self, x, y, width, height, outline, settings, text="", action=None, is_text=0, direction=1):
        super().__init__(x, y, width, height, outline, settings, text, action)
        if is_text or self.text in TEXT_ONLY:
            self.animation = Animation(
                [pygame.transform.scale(sprite_manager.get(f"sprites/words/{self.text}/{self.text}{index + 1}"),
                                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
        else:
            directory = f'./sprites/{self.text}'
            sprite_count = len(
                [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]
            )
            state_count = sprite_count // 3
            letterize = {
                0: 'b',
                1: 'r',
                2: 'f',
                3: 'l',
            }
            if state_count > 4:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.text}/{letterize[direction]}0{index}"),
                                            (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_count > 1:
                self.animation = Animation(
                    [pygame.transform.scale(
                        sprite_manager.get(f"sprites/{self.text}/{letterize[direction]}{index + 1}"),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            else:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.text}/{index + 1}"),
                                            (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))

    def draw(self, screen: pygame.surface.Surface):
        self.animation.update()
        self.animation.draw(screen)
