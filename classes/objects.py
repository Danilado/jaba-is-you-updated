import os
import os.path
from typing import Union

import pygame

from classes.animation import Animation
from elements.global_classes import sprite_manager
from settings import TEXT_ONLY

pygame.font.init()
font = pygame.font.SysFont('segoeuisemibold', 15)


# TODO: Too many fields, refactor this please!
# Абстрактный, но нет
class Object:
    """
    Объект правил, например, jaba, you, is, and, и т.д

    :ivar x: Позиция объекта на **сетке** уровня по оси х
    :ivar y: Позиция объекта на **сетке** уровня по оси y
    :ivar xpx: Абсцисса объекта на **экране** по оси х
    :ivar ypx: Ордината объекта на **экране** по оси y

    :ivar direction:
        Направление, в которое смотрит объект во время создания. Может принимать следующие значения:
        0 - Вверх
        1 - Вправо
        2 - Вниз
        3 - Влево
        Используется с правилами move, turn,
        shift и т.д.

    :ivar name: Название объекта
    :ivar is_text: Переменная определяющая является объект текстом, или нет

    :ivar width: Ширина спрайта
    :ivar height: Высота спрайта
    """
    def debug(self):
        return print(f"""
-- {self.x} {self.y} ---
x:          {self.x}
y:          {self.y}
direction:  {self.direction}
name:       {self.name}
is_text:    {self.name}
--- {(len(str(self.x)) + len(str(self.y))) * ' '} ---
        """)   # TODO: Use logger library

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty", is_text: bool = True):
        """
        Инициализация объекта

        :param x: Позиция объекта на **сетке** уровня по оси х
        :param y: Позиция объекта на **сетке** уровня по оси y

        :param direction:
            Направление, в которое смотрит объект во время создания. Может принимать следующие значения:
            0 - Вверх
            1 - Вправо
            2 - Вниз
            3 - Влево
            Используется с правилами move, turn,
            shift и т.д.

        :param name: Название объекта

        .. important:: По названию определяется и текстурка объекта на поле!

        :param is_text: Переменная определяющая является объект текстом, или нет
        """
        self.name = name
        if self.name in TEXT_ONLY: self.is_text = True
        self.text = is_text 
        self.direction = direction  # Используется с правилами move, turn, shift и т.д.
        self.x = x  # Не по пикселям, а по сетке!
        self.y = y  # Не по пикселям, а по сетке!
        self.xpx = x * 50 if self.x is not None else None  # По пикселям
        self.ypx = y * 50 if self.y is not None else None  # По пикселям
        self.width = 50
        self.height = 50
        self.animation = None
        self.animation_init()

    def animation_init(self):
        if self.text or self.name in TEXT_ONLY:
            self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/words/{self.name}/{self.name}{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
        else:
            DIR = f'./sprites/{self.name}'
            sprite_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            state_count = sprite_count // 3
            letterize = {
                0: 'b',
                1: 'r',
                2: 'f',
                3: 'l',
            }
            if state_count > 4:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.name}/{letterize[self.direction]}0{index}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_count > 1:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.name}/{letterize[self.direction]}{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            else:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.name}/{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))

    def draw(self, screen: Union[pygame.Surface, pygame.surface.Surface]):
        """
        Метод отрисовки кнопки

        :param screen: Surface, на котором будет происходить отрисовка
        """
        self.animation.update()
        self.animation.draw(screen)

    def unparse(self) -> str:
        """Сериализовать объект в строку"""
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'
