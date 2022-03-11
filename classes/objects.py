import os
import os.path
from typing import Optional

import pygame
from typing import List, Tuple, Literal

from classes.animation import Animation
from elements.global_classes import sprite_manager
from global_types import SURFACE
from settings import TEXT_ONLY, LETTERS, PIPES, DEBUG, RESOLUTION, NOUNS, OPERATORS, PROPERTIES


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

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty",
                 is_text: bool = True, turning_side: int = -1):
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
        self.animation: Animation = self.animation_init()
        # TODO: Use enum, and make field private
        self.status_of_rotate: Literal[0, 1, 2, 3] = 0
        self.turning_side: Literal[0, 1, 2, 3, -1] = turning_side
        self.is_hide = False
        self.is_hot = False
        self.locked_sides = []

    def animation_init(self):
        if self.text or self.name in TEXT_ONLY \
                and self.name not in PIPES \
                and self.name not in LETTERS:
            self.animation = Animation(
                [
                    pygame.transform.scale(
                        sprite_manager.get(
                            f"sprites/words/{self.name}/{self.name}{index + 1}"),
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
                self.animation = Animation(
                    [pygame.transform.scale(
                        sprite_manager.get(
                            f"sprites/{self.name}/{letterize[self.direction]}0{index}"),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
            elif state_count > 1:
                self.animation = Animation(
                    [pygame.transform.scale(
                        sprite_manager.get(
                            f"sprites/{self.name}/{letterize[self.direction]}{index + 1}"),
                        (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
            else:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.name}/{index + 1}"),
                                            (50, 50)) for index in range(0, 3)], 200, (self.xpx, self.ypx), True)
        return self.animation

    def draw(self, screen: SURFACE):
        """
        Метод отрисовки кнопки

        :param screen: Surface, на котором будет происходить отрисовка
        """
        if not self.is_hide:
            self.animation.update()
            self.animation.draw(screen)

    def unparse(self) -> str:
        """Сериализовать объект в строку"""
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'

    def move(self, matrix, level_rules):  # TODO: use Δt to calculate distance move
        """Метод движения персонажа"""
        if self.turning_side == 0:
            self.move_right(matrix, level_rules)
        if self.turning_side == 1:
            self.move_up(matrix, level_rules)
        if self.turning_side == 2:
            self.move_left(matrix, level_rules)
        if self.turning_side == 3:
            self.move_down(matrix, level_rules)
        #if DEBUG:
        #    print(self.turning_side, self.status_of_rotate)
        self.animation_init()


    def move_up(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вверх"""
        if self.y > 0:
            if 'up' in self.locked_sides:
                return False
            for objects in matrix[self.y - 1][self.x]:
                for rule in level_rules:
                    if objects.is_hot and f'{self.name} is melt' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                    if f'{objects.name} is defeat' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                if objects.move_up(matrix, level_rules, 'push'):
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.status_of_rotate = 1
                    self.y -= 1
                    self.ypx -= 50
                    self.direction = 0
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        1
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and self.text == False:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.y -= 1
                    self.ypx -= 50
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        1
                    ))
                    return True
            if status_push == None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 1
                self.y -= 1
                self.ypx -= 50
                self.direction = 0
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    1
                ))
            return True


    def move_down(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вниз"""
        if self.y < RESOLUTION[1] // 50 - 1:
            if 'down' in self.locked_sides:
                return False
            for objects in matrix[self.y + 1][self.x]:
                for rule in level_rules:
                    if objects.is_hot and f'{self.name} is melt' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                    if f'{objects.name} is defeat' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                if objects.move_down(matrix, level_rules, 'push'):
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.status_of_rotate = 3
                    self.y += 1
                    self.ypx += 50
                    self.direction = 2
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        3
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and self.text == False:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.y += 1
                    self.ypx += 50
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        3
                    ))
                    return True
            if status_push == None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 3
                self.y += 1
                self.ypx += 50
                self.direction = 2
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    3
                ))
            return True


    def move_left(self, matrix, level_rules, status_push=None):
        """Метод движения персонажа влево"""
        if self.x > 0:
            if 'left' in self.locked_sides:
                return False
            for objects in matrix[self.y][self.x - 1]:
                for rule in level_rules:
                    if objects.is_hot and f'{self.name} is melt' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                    if f'{objects.name} is defeat' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                if objects.move_left(matrix, level_rules, 'push'):
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.status_of_rotate = 2
                    self.x -= 1
                    self.xpx -= 50
                    self.direction = 3
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        2
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and self.text == False:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.x -= 1
                    self.xpx -= 50
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        2
                    ))
                    return True
            if status_push == None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 2
                self.x -= 1
                self.xpx -= 50
                self.direction = 3
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    2
                ))
            return True



    def move_right(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вправо"""
        if self.x < RESOLUTION[0] // 50 - 1:
            if 'right' in self.locked_sides:
                return False
            for objects in matrix[self.y][self.x + 1]:
                for rule in level_rules:
                    if objects.is_hot and f'{self.name} is melt' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                    if f'{objects.name} is defeat' in rule.text_rule:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        return False
                if objects.move_right(matrix, level_rules, 'push'):
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.status_of_rotate = 0
                    self.x += 1
                    self.xpx += 50
                    self.direction = 1
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        0
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and self.text == False:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.x += 1
                    self.xpx += 50
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        0
                    ))
                    return True
            if status_push == None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 0
                self.x += 1
                self.xpx += 50
                self.direction = 1
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    0
                ))
            return True


    def check_events(self, events: List[pygame.event.Event]):
        """Метод обработки событий"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.turning_side = 0
                if event.key == pygame.K_w:
                    self.turning_side = 1
                if event.key == pygame.K_a:
                    self.turning_side = 2
                if event.key == pygame.K_s:
                    self.turning_side = 3


            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a]:
                    self.turning_side = -1

