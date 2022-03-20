from copy import copy
import os
import os.path
from typing import List, Literal

import pygame

from classes.animation import Animation
from elements.global_classes import sprite_manager
from global_types import SURFACE
from settings import TEXT_ONLY, SPRITE_ONLY, RESOLUTION, NOUNS, OPERATORS, PROPERTIES

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
is_text:    {self.is_text}
--- {(len(str(self.x)) + len(str(self.y))) * ' '} ---
        """)  # TODO: Use logger library

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty",
                 is_text: bool = True, movement_state: int = 0, neighbours=None,
                 turning_side: Literal[0, 1, 2, 3, -1] = -1, animation=None,
                 safe=False):
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
        self.is_text = is_text

        self.turning_side = turning_side
        self.status_of_rotate: Literal[0, 1, 2, 3] = 0
        self.direction = direction
        self.direction_key_map = {
            0: 1,
            1: 0,
            2: 3,
            3: 2,
        }

        if neighbours is None:
            neighbours = []
        self.neighbours: List[List[Object]] = neighbours

        self.x = x
        self.y = y
        self.xpx = x * 50
        self.ypx = y * 50

        self.width = 50
        self.height = 50

        self.animation: Animation
        self.movement_state = movement_state
        self.animation = animation

        self.is_hide = False
        self.is_hot = False
        self.is_reverse = False
        self.is_safe = safe
        self.locked_sides = []
        self.is_open = False
        self.is_shut = False
        self.is_phantom = False
        self.status_move = False

        if self.name != 'empty' and self.animation == None:
            self.animation = self.animation_init()

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
                if not object.is_text and object.name == self.name:
                    key += char_dict[index]
        return key_dict[key]

    def animation_init(self) -> Animation:
        """Инициализирует анимацию объекта, основываясь на его имени,
           "Текстовом состоянии", направлении, стадии движения и т.д.
        """
        animation = Animation([], 200, (self.xpx, self.ypx))
        if (self.is_text or self.name in TEXT_ONLY) and self.name not in SPRITE_ONLY:
            path = os.path.join('./', 'sprites', 'text')
            animation.sprites = [pygame.transform.scale(sprite_manager.get(
                os.path.join(f"{path}", self.name, f"{self.name}_0_{index + 1}")),
                (50, 50)) for index in range(0, 3)]
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

            try:
                if state_max == 0:
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_0_{index}')),
                        (50, 50)) for index in range(1, 4)]
                elif state_max == 15:
                    frame = self.investigate_neighbours()
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{frame}_{index}')),
                        (50, 50)) for index in range(1, 4)]
                elif state_max == 3:
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.movement_state % 4}_{index}')),
                        (50, 50)) for index in range(1, 4)]
                elif state_max == 24:
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_{self.direction_key_map[self.direction] * 8}_{index}')),
                        (50, 50)) for index in range(1, 4)]
                elif state_max == 27:
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(path,
                                     f'{self.name}_'
                                     f'{self.movement_state % 4 + self.direction_key_map[self.direction] * 8}_'
                                     f'{index}')),
                        (50, 50)) for index in range(1, 4)]
                elif state_max == 31:
                    animation.sprites = [pygame.transform.scale(sprite_manager.get(
                        os.path.join(
                            path,
                            f'{self.name}_'
                            f'{self.movement_state % 4 + max(self.direction_key_map[self.direction] * 8, 0)}_'
                            f'{index}')),
                        (50, 50)) for index in range(1, 4)]
                else:
                    print(f'{self.name} somehow fucked up while setting animation')
            except FileNotFoundError:
                if self.movement_state == 0:
                    print(f'{self.name} somehow fucked up while setting animation')
                else:
                    self.movement_state = 0
                    return self.animation_init()
        return animation

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
        return f'{self.x} {self.y} {self.direction} {self.name} {self.is_text}'

    def get_index(self, matrix):
        for i in range(len(matrix[self.y][self.x])):
            if matrix[self.y][self.x][i].name == self.name:
                return i

    def move(self, matrix, level_rules):
        """Метод движения персонажа"""
        if self.turning_side == 0:
            self.move_right(matrix, level_rules)
            self.direction = 1
        elif self.turning_side == 1:
            self.move_up(matrix, level_rules)
            self.direction = 0
        elif self.turning_side == 2:
            self.move_left(matrix, level_rules)
            self.direction = 3
        elif self.turning_side == 3:
            self.move_down(matrix, level_rules)
            self.direction = 2

    def move_up(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вверх"""
        if self.y > 0:
            if 'up' in self.locked_sides:
                return False
            for objects in matrix[self.y - 1][self.x]:
                for rule in level_rules:
                    if f'{objects.name} is swap' in rule.text_rule or (
                            f'{self.name} is swap' in rule.text_rule and not self.is_phantom):
                        matrix[self.y][self.x].pop(self.get_index(matrix))
                        self.status_of_rotate = 1
                        self.y -= 1
                        self.ypx -= 50
                        self.direction = 0
                        self.movement_state += 1
                        objects.y += 1
                        objects.movement_state += 1
                        self.animation = None
                        objects.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        matrix[self.y + 1][self.x].append(copy(objects))
                        matrix[self.y][self.x].pop(objects.get_index(matrix))
                        return False
                if not self.is_safe:
                    for rule in level_rules:
                        if f'{self.name} is melt' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is hot' in sec_rule.text_rule:
                                    matrix[self.y][self.x].pop(
                                        self.get_index(matrix))
                                    return False

                    for rule in level_rules:
                        if self.is_open and f'{objects.name} is shut' in rule.text_rule \
                                or self.is_shut and f'{objects.name} is open' in rule.text_rule:
                            matrix[self.y][self.x].pop(self.get_index(matrix))
                            matrix[self.y -
                                   1][self.x].pop(objects.get_index(matrix))
                            return False

                    for rule in level_rules:
                        if f'{objects.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{self.name} is you' in sec_rule.text_rule:
                                    for i in range(len(matrix[self.y][self.x])):
                                        if matrix[self.y][self.x][i].name == self.name:
                                            matrix[self.y][self.x].pop(i)
                                    return False

                    for rule in level_rules:
                        if f'{self.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is you' in sec_rule.text_rule:
                                    matrix[self.y -
                                           1][self.x].pop(objects.get_index(matrix))
                                    return False

                for rule in level_rules:
                    if self.is_hot and f'{objects.name} is melt' in rule.text_rule:
                        matrix[self.y -
                               1][self.x].pop(objects.get_index(matrix))

                for rule in level_rules:
                    if self.is_open and f'{objects.name} is shut' in rule.text_rule \
                            or self.is_shut and f'{objects.name} is open' in rule.text_rule:
                        matrix[self.y][self.x].pop(self.get_index(
                            matrix)) if not self.is_safe else ...
                        matrix[self.y -
                               1][self.x].pop(objects.get_index(matrix))
                        if not self.is_safe:
                            return False
                        else:
                            self.move_up(matrix, level_rules)
                objects_is_stop = False
                for rule in level_rules:
                    if f'{objects.name} is stop' in rule.text_rule or f'{objects.name} is pull' in rule.text_rule \
                            or objects.name in OPERATORS or objects.name in PROPERTIES or (
                            objects.name in NOUNS and objects.is_text) \
                            or f'{objects.name} is push' in rule.text_rule:
                        objects_is_stop = True
                can_move = False
                for rule in level_rules:
                    if f'{self.name} is move' in rule.text_rule \
                            or f'{self.name} is push' in rule.text_rule \
                            or f'{self.name} is auto' in rule.text_rule \
                            or f'{self.name} is nudge' in rule.text_rule \
                            or f'{self.name} is chill' in rule.text_rule \
                            or f'{self.name} is you' in rule.text_rule \
                            or self.name in OPERATORS or self.name in PROPERTIES or (
                            self.name in NOUNS and self.is_text) and objects.y != 0:
                        can_move = True
                if self.is_phantom or not objects_is_stop:
                    if can_move:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.y < RESOLUTION[1] // 50 - 1:
                            for pull_object in matrix[self.y + 1][self.x]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_up(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 1
                        self.y -= 1
                        self.ypx -= 50
                        self.direction = 0
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                    return True
                if can_move:
                    if objects.move_up(matrix, level_rules, 'push'):

                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.y < RESOLUTION[1] // 50 - 1:
                            for pull_object in matrix[self.y + 1][self.x]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_up(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 1
                        self.y -= 1
                        self.ypx -= 50
                        self.direction = 0
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        return True
                return False
            for rule in level_rules:
                if f'{self.name} is pull' in rule.text_rule and status_push == 'pull' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    if self.y < RESOLUTION[1] // 50 - 1:
                        for pull_object in matrix[self.y + 1][self.x]:
                            if not pull_object.is_text and pull_object.name in NOUNS:
                                pull_object.move_up(
                                    matrix, level_rules, 'pull')
                    self.status_of_rotate = 0
                    self.y -= 1
                    self.ypx -= 50
                    self.direction = 0
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            for rule in level_rules:
                if ((f'{self.name} is stop' in rule.text_rule and status_push == 'push')
                    or (f'{self.name} is pull' in rule.text_rule and status_push == 'push')) \
                        and not self.is_text:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.y -= 1
                    self.ypx -= 50
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.is_text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                    if self.y < RESOLUTION[1] // 50 - 1:
                        for pull_object in matrix[self.y + 1][self.x]:
                            if not pull_object.is_text and pull_object.name in NOUNS:
                                pull_object.move_up(
                                    matrix, level_rules, 'pull')
                self.status_of_rotate = 1
                self.y -= 1
                self.ypx -= 50
                self.direction = 0
                self.movement_state += 1
                self.animation = None
                matrix[self.y][self.x].append(copy(self))
            return True

    def move_down(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вниз"""
        if self.y < RESOLUTION[1] // 50 - 1:
            if 'down' in self.locked_sides:
                return False
            for objects in matrix[self.y + 1][self.x]:
                for rule in level_rules:
                    if f'{objects.name} is swap' in rule.text_rule \
                            or (f'{self.name} is swap' in rule.text_rule and not self.is_phantom):
                        matrix[self.y][self.x].pop(self.get_index(matrix))
                        self.status_of_rotate = 3
                        self.y += 1
                        self.ypx += 50
                        self.direction = 2
                        self.movement_state += 1
                        objects.y -= 1,
                        objects.movement_state += 1
                        self.animation = None
                        objects.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        matrix[self.y - 1][self.x].append(copy(objects))
                        matrix[self.y][self.x].pop(objects.get_index(matrix))
                        return False

                if not self.is_safe:
                    for rule in level_rules:
                        if f'{self.name} is melt' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is hot' in sec_rule.text_rule:
                                    matrix[self.y][self.x].pop(
                                        self.get_index(matrix))
                                    return False

                    for rule in level_rules:
                        if f'{objects.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{self.name} is you' in sec_rule.text_rule:
                                    for i in range(len(matrix[self.y][self.x])):
                                        if matrix[self.y][self.x][i].name == self.name:
                                            matrix[self.y][self.x].pop(i)
                                    return False

                    for rule in level_rules:
                        if f'{self.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is you' in sec_rule.text_rule:
                                    matrix[self.y +
                                           1][self.x].pop(objects.get_index(matrix))
                                    return False

                for rule in level_rules:
                    if self.is_hot and f'{objects.name} is melt' in rule.text_rule:
                        matrix[self.y +
                               1][self.x].pop(objects.get_index(matrix))

                for rule in level_rules:
                    if self.is_open and f'{objects.name} is shut' in rule.text_rule \
                            or self.is_shut and f'{objects.name} is open' in rule.text_rule:
                        matrix[self.y][self.x].pop(self.get_index(
                            matrix)) if not self.is_safe else ...
                        matrix[self.y +
                               1][self.x].pop(objects.get_index(matrix))
                        if not self.is_safe:
                            return False
                        else:
                            self.move_down(matrix, level_rules)
                objects_is_stop = False
                for rule in level_rules:
                    if f'{objects.name} is stop' in rule.text_rule or f'{objects.name} is pull' in rule.text_rule \
                            or objects.name in OPERATORS or objects.name in PROPERTIES or (
                            objects.name in NOUNS and objects.is_text) \
                            or f'{objects.name} is push' in rule.text_rule:
                        objects_is_stop = True
                can_move = False
                for rule in level_rules:
                    if f'{self.name} is move' in rule.text_rule \
                            or f'{self.name} is push' in rule.text_rule \
                            or f'{self.name} is auto' in rule.text_rule \
                            or f'{self.name} is nudge' in rule.text_rule \
                            or f'{self.name} is chill' in rule.text_rule \
                            or f'{self.name} is you' in rule.text_rule \
                            or self.name in OPERATORS or self.name in PROPERTIES or (
                            self.name in NOUNS and self.is_text) and objects.y != RESOLUTION[1] // 50 - 1:
                        can_move = True
                if self.is_phantom or not objects_is_stop:
                    if can_move:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.y > 0:
                            for pull_object in matrix[self.y - 1][self.x]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_down(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 3
                        self.y += 1
                        self.ypx += 50
                        self.direction = 2
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                    return True
                if can_move:
                    if objects.move_down(matrix, level_rules, 'push'):
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.y > 0:
                            for pull_object in matrix[self.y - 1][self.x]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_down(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 3
                        self.y += 1
                        self.ypx += 50
                        self.direction = 2
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        return True
                return False

            for rule in level_rules:
                if f'{self.name} is pull' in rule.text_rule and status_push == 'pull' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    if self.y > 0:
                        for pull_object in matrix[self.y - 1][self.x]:
                            if not pull_object.is_text and pull_object.name in NOUNS:
                                pull_object.move_down(
                                    matrix, level_rules, 'pull')
                    self.status_of_rotate = 0
                    self.y += 1
                    self.ypx += 50
                    self.direction = 2
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            for rule in level_rules:
                if ((f'{self.name} is stop' in rule.text_rule and status_push == 'push')
                    or (f'{self.name} is pull' in rule.text_rule and status_push == 'push')) \
                        and not self.is_text:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.y += 1
                    self.ypx += 50
                    self.direction = 2
                    self.movement_state + 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.is_text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                if self.y > 0:
                    for pull_object in matrix[self.y - 1][self.x]:
                        if not pull_object.is_text and pull_object.name in NOUNS:
                            pull_object.move_down(matrix, level_rules, 'pull')
                self.status_of_rotate = 3
                self.y += 1
                self.ypx += 50
                self.direction = 2
                self.movement_state += 1
                self.animation = None
                matrix[self.y][self.x].append(copy(self))
            return True

    def move_left(self, matrix, level_rules, status_push=None):
        """Метод движения персонажа влево"""
        if self.x > 0:
            if 'left' in self.locked_sides:
                return False
            for objects in matrix[self.y][self.x - 1]:
                for rule in level_rules:
                    if f'{objects.name} is swap' in rule.text_rule or \
                            (f'{self.name} is swap' in rule.text_rule and not self.is_phantom):
                        matrix[self.y][self.x].pop(self.get_index(matrix))
                        self.status_of_rotate = 2
                        self.x -= 1
                        self.xpx -= 50
                        self.direction = 3
                        self.movement_state += 1
                        objects.x += 1
                        objects.movement_state += 1
                        self.animation = None
                        objects.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        matrix[self.y][self.x + 1].append(copy(objects))
                        matrix[self.y][self.x].pop(objects.get_index(matrix))
                        return False

                if not self.is_safe:
                    for rule in level_rules:
                        if f'{self.name} is melt' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is hot' in sec_rule.text_rule:
                                    matrix[self.y][self.x].pop(
                                        self.get_index(matrix))
                                    return False

                    for rule in level_rules:
                        if f'{objects.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{self.name} is you' in sec_rule.text_rule:
                                    for i in range(len(matrix[self.y][self.x])):
                                        if matrix[self.y][self.x][i].name == self.name:
                                            matrix[self.y][self.x].pop(i)
                                    return False

                    for rule in level_rules:
                        if f'{self.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is you' in sec_rule.text_rule:
                                    matrix[self.y][self.x -
                                                   2].pop(objects.get_index(matrix))
                                    return False

                for rule in level_rules:
                    if self.is_hot and f'{objects.name} is melt' in rule.text_rule:
                        matrix[self.y][self.x -
                                       1].pop(objects.get_index(matrix))

                for rule in level_rules:
                    if self.is_open and f'{objects.name} is shut' in rule.text_rule \
                            or self.is_shut and f'{objects.name} is open' in rule.text_rule:
                        matrix[self.y][self.x].pop(self.get_index(
                            matrix)) if not self.is_safe else ...
                        matrix[self.y][self.x -
                                       1].pop(objects.get_index(matrix))
                        if not self.is_safe:
                            return False
                        else:
                            self.move_left(matrix, level_rules)
                objects_is_stop = False
                for rule in level_rules:
                    if f'{objects.name} is stop' in rule.text_rule or f'{objects.name} is pull' in rule.text_rule \
                            or objects.name in OPERATORS or objects.name in PROPERTIES or (
                            objects.name in NOUNS and objects.is_text) \
                            or f'{objects.name} is push' in rule.text_rule:
                        objects_is_stop = True
                can_move = False
                for rule in level_rules:
                    if f'{self.name} is move' in rule.text_rule \
                            or f'{self.name} is push' in rule.text_rule \
                            or f'{self.name} is auto' in rule.text_rule \
                            or f'{self.name} is nudge' in rule.text_rule \
                            or f'{self.name} is chill' in rule.text_rule \
                            or f'{self.name} is you' in rule.text_rule \
                            or self.name in OPERATORS or self.name in PROPERTIES or (
                            self.name in NOUNS and self.is_text) and objects.x != 0:
                        can_move = True
                if self.is_phantom or not objects_is_stop:
                    if can_move:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.x < RESOLUTION[0] // 50 - 1:
                            for pull_object in matrix[self.y][self.x + 1]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_left(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 2
                        self.x -= 1
                        self.xpx -= 50
                        self.direction = 3
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                    return True
                if can_move:
                    if objects.move_left(matrix, level_rules, 'push'):

                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.x < RESOLUTION[0] // 50 - 1:
                            for pull_object in matrix[self.y][self.x + 1]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_left(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 2
                        self.x -= 1
                        self.xpx -= 50
                        self.direction = 3
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        return True
                return False
            for rule in level_rules:
                if f'{self.name} is pull' in rule.text_rule and status_push == 'pull' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    if self.x < RESOLUTION[0] // 50 - 1:
                        for pull_object in matrix[self.y][self.x + 1]:
                            if not pull_object.is_text and pull_object.name in NOUNS:
                                pull_object.move_left(
                                    matrix, level_rules, 'pull')
                    self.status_of_rotate = 0
                    self.x -= 1
                    self.xpx -= 50
                    self.direction = 3
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            for rule in level_rules:
                if ((f'{self.name} is stop' in rule.text_rule and status_push == 'push')
                    or (f'{self.name} is pull' in rule.text_rule and status_push == 'push')) \
                        and not self.is_text:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.x -= 1
                    self.xpx -= 50
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.is_text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                if self.x < RESOLUTION[0] // 50 - 1:
                    for pull_object in matrix[self.y][self.x + 1]:
                        if not pull_object.is_text and pull_object.name in NOUNS:
                            pull_object.move_left(matrix, level_rules, 'pull')
                self.status_of_rotate = 2
                self.x -= 1
                self.xpx -= 50
                self.direction = 3
                self.movement_state += 1
                self.animation = None
                matrix[self.y][self.x].append(copy(self))
            return True

    def move_right(self, matrix, level_rules, status_push=None):
        """Метод движения объекта вправо"""
        if self.x < RESOLUTION[0] // 50 - 1:
            if 'right' in self.locked_sides:
                return False
            for objects in matrix[self.y][self.x + 1]:
                for rule in level_rules:
                    if f'{objects.name} is swap' in rule.text_rule \
                            or (f'{self.name} is swap' in rule.text_rule and not self.is_phantom):
                        matrix[self.y][self.x].pop(self.get_index(matrix))
                        self.status_of_rotate = 0
                        self.x += 1
                        self.xpx += 50
                        self.direction = 1
                        self.movement_state += 1
                        objects.x -= 1
                        objects.movement_state += 1
                        self.animation = None
                        objects.animation = None
                        matrix[self.y][self.x].append(copy(self))
                        matrix[self.y][self.x - 1].append(copy(objects))
                        matrix[self.y][self.x].pop(objects.get_index(matrix))
                        return False
                if not self.is_safe:
                    for rule in level_rules:
                        if f'{self.name} is melt' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is hot' in sec_rule.text_rule:
                                    matrix[self.y][self.x].pop(
                                        self.get_index(matrix))
                                    return False

                    for rule in level_rules:
                        if f'{objects.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{self.name} is you' in sec_rule.text_rule:
                                    for i in range(len(matrix[self.y][self.x])):
                                        if matrix[self.y][self.x][i].name == self.name:
                                            matrix[self.y][self.x].pop(i)
                                    return False

                    for rule in level_rules:
                        if f'{self.name} is defeat' in rule.text_rule:
                            for sec_rule in level_rules:
                                if f'{objects.name} is you' in sec_rule.text_rule:
                                    matrix[self.y][self.x -
                                                   2].pop(objects.get_index(matrix))
                                    return False

                for rule in level_rules:
                    if (self.is_hot and f'{objects.name} is melt' in rule.text_rule):
                        matrix[self.y][self.x -
                                       1].pop(objects.get_index(matrix))

                for rule in level_rules:
                    if self.is_open and f'{objects.name} is shut' in rule.text_rule \
                            or self.is_shut and f'{objects.name} is open' in rule.text_rule:
                        matrix[self.y][self.x].pop(self.get_index(
                            matrix)) if not self.is_safe else ...
                        matrix[self.y][self.x +
                                       1].pop(objects.get_index(matrix))
                        if not self.is_safe:
                            return False
                        else:
                            self.move_right(matrix, level_rules)
                objects_is_stop = False
                for rule in level_rules:
                    if f'{objects.name} is stop' in rule.text_rule or f'{objects.name} is pull' in rule.text_rule \
                            or objects.name in OPERATORS or objects.name in PROPERTIES or (
                            objects.name in NOUNS and objects.is_text) \
                            or f'{objects.name} is push' in rule.text_rule:
                        objects_is_stop = True
                can_move = False
                for rule in level_rules:
                    if f'{self.name} is move' in rule.text_rule \
                            or f'{self.name} is push' in rule.text_rule \
                            or f'{self.name} is auto' in rule.text_rule \
                            or f'{self.name} is nudge' in rule.text_rule \
                            or f'{self.name} is chill' in rule.text_rule \
                            or f'{self.name} is you' in rule.text_rule \
                            or self.name in OPERATORS or self.name in PROPERTIES or (
                            self.name in NOUNS and self.is_text) and objects.x != RESOLUTION[0] // 50 - 1:
                        can_move = True
                if not objects_is_stop or self.is_phantom:
                    if can_move:
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.x > 0:
                            for pull_object in matrix[self.y][self.x - 1]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_right(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 0
                        self.x += 1
                        self.xpx += 50
                        self.direction = 1
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                    return True
                if can_move:
                    if objects.move_right(matrix, level_rules, 'push'):
                        for i in range(len(matrix[self.y][self.x])):
                            if matrix[self.y][self.x][i].name == self.name:
                                matrix[self.y][self.x].pop(i)
                        if self.x > 0:
                            for pull_object in matrix[self.y][self.x - 1]:
                                if not pull_object.is_text and pull_object.name in NOUNS:
                                    pull_object.move_right(
                                        matrix, level_rules, 'pull')
                        self.status_of_rotate = 0
                        self.x += 1
                        self.xpx += 50
                        self.direction = 1
                        self.movement_state += 1
                        self.animation = None
                        matrix[self.y][self.x].append(copy(self))
                    return True
            for rule in level_rules:
                if f'{self.name} is pull' in rule.text_rule and status_push == 'pull' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    if self.x > 0:
                        for pull_object in matrix[self.y][self.x - 1]:
                            if not pull_object.is_text and pull_object.name in NOUNS:
                                pull_object.move_right(
                                    matrix, level_rules, 'pull')
                    self.status_of_rotate = 0
                    self.x += 1
                    self.xpx += 50
                    self.direction = 1
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            for rule in level_rules:
                if ((f'{self.name} is stop' in rule.text_rule and status_push == 'push')
                    or (f'{self.name} is pull' in rule.text_rule and status_push == 'push')) \
                        and not self.is_text:
                    return False
            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status_push == 'push':
                    for i in range(len(matrix[self.y][self.x])):
                        if matrix[self.y][self.x][i].name == self.name:
                            matrix[self.y][self.x].pop(i)
                    self.x += 1
                    self.xpx += 50
                    self.movement_state += 1
                    self.animation = None
                    matrix[self.y][self.x].append(copy(self))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.is_text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                if self.x > 0:
                    for pull_object in matrix[self.y][self.x - 1]:
                        if not pull_object.is_text and pull_object.name in NOUNS:
                            pull_object.move_right(matrix, level_rules, 'pull')
                self.status_of_rotate = 0
                self.x += 1
                self.xpx += 50
                self.direction = 1
                self.movement_state += 1
                self.animation = None
                matrix[self.y][self.x].append(copy(self))
                return True
            return False


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

    @property
    def is_operator(self) -> bool:
        return self.name in OPERATORS

    @property
    def is_property(self) -> bool:
        return self.name in PROPERTIES

    @property
    def is_noun(self) -> bool:
        return self.name in NOUNS and self.name not in OPERATORS and self.is_text

    @property
    def special_text(self) -> bool:
        return self.is_text or self.name in TEXT_ONLY

    def __copy__(self):
        copy = Object(
            x=self.x,
            y=self.y,
            direction=self.direction,
            name=self.name,
            is_text=self.is_text,
            movement_state=self.movement_state,
            neighbours=None,
            turning_side=self.turning_side,
            animation=self.animation,
            safe=self.is_safe
        )
        return copy
