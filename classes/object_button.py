import os

import pygame

from classes.animation import Animation
from classes.button import Button
from elements.global_classes import sprite_manager
from settings import TEXT_ONLY, SPRITE_ONLY


class ObjectButton(Button):
    """
    Класс 2-й кнопки, предназначенной для отлавливания нажатий в редакторе карт.
    Эта кнопка отличается от прошлой, тем что имеем свойства как и у :class:`~classes.objects.GameObject`.

    :ivar x: Абсцисса положения
    :ivar y: Ордината положения
    :ivar width: Ширина в пикселях
    :ivar height: Высота в пикселях
    :ivar outline: Цвет контура
    :ivar settings: Настройка цветов
    :ivar text: Текст
    :ivar action: Функция вызывающаяся при нажатии
    :ivar is_text: Есть ли воплощение кнопки в виде блока
    :ivar direction: Направление кнопки
    """

    def __init__(self, x, y, width, height, outline, settings, text="", action=None,
                 is_text=0, direction=0, movement_state=0):
        super().__init__(x, y, width, height, outline, settings, text, action)
        self.is_text = is_text
        self.direction = direction
        self.movement_state = movement_state
        self.animation = None
        self.animation_init()

    def animation_init(self) -> None:
        if (self.is_text or self.text in TEXT_ONLY) and self.text not in SPRITE_ONLY:
            path = os.path.join('./', 'sprites', 'text')
            self.animation = Animation(
                [pygame.transform.scale(sprite_manager.get(
                                        os.path.join(f"{path}", self.text, f"{self.text}_0_{index + 1}")),
                                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
        else:
            path = os.path.join('./', 'sprites', self.text)
            try:
                states = [int(name.split('_')[1]) for name in os.listdir(path) if os.path.isfile(
                    os.path.join(path, name))]
                state_max = max(states)
            except IndexError:
                print(
                    f'{self.text} fucked up while counting states -> probably filename is invalid')
                state_max = 0
            except FileNotFoundError:
                print(
                    f"{self.text} fucked up while searching for files. Probably folder is corrupt or \
                    does not exist. This shouldn't happen in any circumstances")
                state_max = 0

            if state_max in (0, 15):
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.text}_0_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_max == 3:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.text}_{self.movement_state % 4}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_max == 24:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.text}_{self.direction * 8}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_max == 27:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.text}_{self.movement_state % 4 + self.direction * 8}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_max == 31:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.text}_{self.movement_state % 4 + max(self.direction * 8, 0)}\
                                        _{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            else:
                print(f'{self.text} somehow fucked up while setting animation')

    def draw(self, screen: pygame.surface.Surface):
        self.animation.update()
        self.animation.draw(screen)
