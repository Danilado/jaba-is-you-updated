import os
import os.path

import pygame

from classes.animation import Animation
from elements.global_classes import sprite_manager
from global_types import SURFACE
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

    :ivar animation: Анимация объекта
    """

    def debug(self):
        return print(f"""
-- {self.x} {self.y} ---
x:          {self.x}
y:          {self.y}
direction:  {self.direction}
name:       {self.name}
is_text:    {self.text}
--- {(len(str(self.x)) + len(str(self.y))) * ' '} ---
        """)  # TODO: Use logger library

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
        self.name: str = name
        if self.name in TEXT_ONLY:
            self.is_text: bool = True
        self.text: bool = is_text
        self.direction: int = direction  # Используется с правилами move, turn, shift и т.д.
        self.x: int = x  # Не по пикселям, а по сетке!
        self.y: int = y  # Не по пикселям, а по сетке!
        self.xpx: int = x * 50 if self.x is not None else None  # По пикселям
        self.ypx: int = y * 50 if self.y is not None else None  # По пикселям
        self.width: int = 50
        self.height: int = 50
        self.animation: Animation = self.animation_init()

    def animation_init(self) -> Animation:
        """
        Инициализация анимации и спрайтов

        :return: Анимацию
        """
        if self.text or self.name in TEXT_ONLY:
            animation = Animation(
                [
                    pygame.transform.scale(
                        sprite_manager.get(f"sprites/words/{self.name}/{self.name}{index + 1}"),
                        (50, 50)
                    ) for index in range(0, 3)
                ], 200, (self.xpx, self.ypx), True
            )
        else:
            directory = f'./sprites/{self.name}'
            sprite_count = len([name for name in os.listdir(directory)
                                if os.path.isfile(os.path.join(directory, name))])
            state_count = sprite_count // 3
            letterize = {
                0: 'b',
                1: 'r',
                2: 'f',
                3: 'l',
            }
            if state_count > 4:
                animation = Animation(
                    [pygame.transform.scale(
                        sprite_manager.get(f"sprites/{self.name}/{letterize[self.direction]}0{index}"),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
            elif state_count > 1:
                animation = Animation(
                    [pygame.transform.scale(
                        sprite_manager.get(f"sprites/{self.name}/{letterize[self.direction]}{index + 1}"),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
            else:
                animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.name}/{index + 1}"),
                                            (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
        return animation

    def draw(self, screen: SURFACE):
        """
        Метод отрисовки кнопки

        :param screen: Surface, на котором будет происходить отрисовка
        """
        self.animation.update()
        self.animation.draw(screen)

    def unparse(self) -> str:
        """Сериализовать объект в строку"""
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'
