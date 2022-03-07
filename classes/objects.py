import os
import os.path

import pygame

from classes.animation import Animation
from elements.global_classes import sprite_manager
from global_types import SURFACE
from settings import TEXT_ONLY, SPRITE_ONLY

pygame.font.init()
font = pygame.font.SysFont('segoeuisemibold', 15)


# TODO: Too many fields, refactor this please!
# Gospodin: Отнюдь.
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

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty",
                 is_text: bool = True, movement_state: int = 0, neighbours=[]):
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
            self.is_text = True
        self.text = is_text
        # Используется с правилами move, turn, shift и т.д.
        self.direction = direction
        self.x = x  # Не по пикселям, а по сетке!
        self.y = y  # Не по пикселям, а по сетке!
        self.xpx = x * 50  # По пикселям
        self.ypx = y * 50  # По пикселям
        self.width = 50
        self.height = 50
        self.animation: Animation
        self.movement_state = movement_state
        self.neighbours = neighbours
        if self.name != 'empty':
            self.animation_init()

    def investigate_neighbours(self):
        """Исследует соседей объекта и возвращает правильный ключ к спрайту

        :return: Ключ для правильного выбора спрайтов и анимации
        :rtype: int
        """
        key_dict = {
            '': 0,
            'r': 1,
            'u': 2,
            'ur': 3,
            'l': 4,
            'rl': 5,
            'ul': 6,
            'url': 7,
            'b': 8,
            'rb': 9,
            'ub': 10,
            'urb': 11,
            'bl': 12,
            'rbl': 13,
            'ubl': 14,
            'urbl': 15
        }
        char_dict = ['u', 'r', 'b', 'l']
        key = ''
        for index, array in enumerate(self.neighbours):
            for object in array:
                if not object.text and object.name == self.name:
                    key += char_dict[index]
        return key_dict[key]

    def animation_init(self):
        """Инициализирует анимацию объекта, основываясь на его имени,
           "Текстовом состоянии", направлении, стадии движения и т.д.
        """
        if (self.text or self.name in TEXT_ONLY) and self.name not in SPRITE_ONLY:
            path = os.path.join('./', 'sprites', 'text')
            self.animation = Animation(
                [pygame.transform.scale(sprite_manager.get(
                    os.path.join(f"{path}", self.name, f"{self.name}_0_{index + 1}")),
                    (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
        else:
            path = os.path.join('./', 'sprites', self.name)
            try:
                states = [int(name.split('_')[1]) for name in os.listdir(path) if os.path.isfile(
                    os.path.join(path, name))]
                state_max = max(states)
            except IndexError:
                print(
                    f'{self.name} fucked up while counting states -> probably filename is invalid')
                state_max = 0
            except FileNotFoundError:
                print(
                    f"{self.name} fucked up while searching for files. Probably folder is corrupt or \
                    does not exist. This shouldn't happen in any circumstances")
                state_max = 0

            if state_max == 0:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_0_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_max == 15:
                frame = self.investigate_neighbours()
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{frame}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_max == 3:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.movement_state % 4}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_max == 24:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.direction * 8}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_max == 27:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.movement_state % 4 + self.direction * 8}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            elif state_max == 31:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.movement_state % 4 + max(self.direction * 8, 0)}_{index + 1}')),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx))
            else:
                print(f'{self.name} somehow fucked up while setting animation')

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
