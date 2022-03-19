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
is_text:    {self.text}
--- {(len(str(self.x)) + len(str(self.y))) * ' '} ---
        """)  # TODO: Use logger library

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty",  # This isn't pythonic way.
                 # TODO: Use None instead of "empty"
                 is_text: bool = True, movement_state: int = 0, neighbours=None,
                 turning_side: Literal[0, 1, 2, 3, -1] = -1):
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
        self.text = is_text  # TODO: Rename text to is_text.
        # Используется с правилами move, turn, shift и т.д.
        self.direction = direction
        self.direction_key_map = {
            0: 1,
            1: 0,
            2: 3,
            3: 2,
        }
        if neighbours is None:
            neighbours = []

        self.turning_side = turning_side
        self.x = x  # Не по пикселям, а по сетке!
        self.y = y  # Не по пикселям, а по сетке!
        self.xpx = x * 50  # По пикселям
        self.ypx = y * 50  # По пикселям
        self.width = 50
        self.height = 50
        self.animation: Animation
        self.movement_state = movement_state
        self.neighbours: List[List[Object]] = neighbours
        self.status_of_rotate: Literal[0, 1, 2, 3] = 0
        self.turning_side: Literal[0, 1, 2, 3, -1] = turning_side
        self.is_hide = False
        self.is_hot = False
        self.locked_sides = []
        self.angle_3d = -90 + 90 * self.direction
        self.animation = None
        if self.name != 'empty':
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
                if not object.text and object.name == self.name:
                    key += char_dict[index]
        return key_dict[key]

    def animation_init(self) -> Animation:
        """Инициализирует анимацию объекта, основываясь на его имени,
           "Текстовом состоянии", направлении, стадии движения и т.д.
        """
        animation = Animation([], 200, (self.xpx, self.ypx))
        if (self.text or self.name in TEXT_ONLY) and self.name not in SPRITE_ONLY:
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
                    return self.animation_init()  # quswadress: Но зачем?
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
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'

    def move(self, matrix, level_rules, flag_3d):
        if flag_3d:
            self.move_3d(matrix, level_rules, flag_3d)
        else:
            self.move_2d(matrix, level_rules, flag_3d)

    def move_2d(self, matrix, level_rules, flag_3d):  # TODO: use Δt to calculate distance move
        """Метод движения персонажа"""
        moved = False
        if self.turning_side == 0:
            self.move_right(matrix, level_rules, flag_3d=flag_3d)
            self.direction = 1
            moved = True
        elif self.turning_side == 1:
            self.move_up(matrix, level_rules, flag_3d=flag_3d)
            self.direction = 0
            moved = True
        elif self.turning_side == 2:
            self.move_left(matrix, level_rules, flag_3d=flag_3d)
            self.direction = 3
            moved = True
        elif self.turning_side == 3:
            self.move_down(matrix, level_rules, flag_3d=flag_3d)
            self.direction = 2
            moved = True
        if moved:
            self.movement_state += 1
            self.animation_init()
            self.turning_side = -1

    def move_3d(self, matrix, level_rules, flag_3d):  # TODO: use Δt to calculate distance move
        moved = False
        if self.turning_side == 2:
            self.angle_3d = (self.angle_3d - 90) % 360

        elif self.turning_side == 0:
            self.angle_3d = (self.angle_3d + 90) % 360

        elif self.turning_side == 1:
            if self.angle_3d == 0:
                self.direction = 1
                self.move_right(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == 180 or self.angle_3d == -180:
                self.direction = 3
                self.move_left(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == 90 or self.angle_3d == -270:
                self.direction = 2
                self.move_down(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == -90 or self.angle_3d == 270:
                self.direction = 0
                self.move_up(matrix, level_rules, flag_3d=flag_3d)
            moved = True
        elif self.turning_side == 3:
            if self.angle_3d == 0:
                self.direction = 1
                self.move_left(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == 180 or self.angle_3d == -180:
                self.direction = 3
                self.move_right(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == 90 or self.angle_3d == -270:
                self.direction = 2
                self.move_up(matrix, level_rules, flag_3d=flag_3d)
            if self.angle_3d == -90 or self.angle_3d == 270:
                self.direction = 0
                self.move_down(matrix, level_rules, flag_3d=flag_3d)
            moved = True
        if moved:
            self.movement_state += 1
            self.animation_init()
        self.turning_side = -1

    def move_up(self, matrix, level_rules, status_push=None, flag_3d=False):
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
                    if not flag_3d:
                        self.direction = 0
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        self.movement_state + 1
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and not self.text:
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
                        self.movement_state + 1
                    ))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 1
                self.y -= 1
                self.ypx -= 50
                if not flag_3d:
                    self.direction = 0
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    self.movement_state + 1
                ))
            return True

    def move_down(self, matrix, level_rules, status_push=None, flag_3d=False):
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
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        self.movement_state + 1
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and not self.text:
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
                        self.movement_state + 1
                    ))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 3
                self.y += 1
                self.ypx += 50
                if not flag_3d:
                    self.direction = 2
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    self.movement_state + 1
                ))
            return True

    def move_left(self, matrix, level_rules, status_push=None, flag_3d=False):
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
                    if not flag_3d:
                        self.direction = 3
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        self.movement_state + 1
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and not self.text:
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
                        self.movement_state + 1
                    ))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 2
                self.x -= 1
                self.xpx -= 50
                if not flag_3d:
                    self.direction = 3
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    self.movement_state + 1
                ))
            return True

    def move_right(self, matrix, level_rules, status_push=None, flag_3d=False):
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
                    if not flag_3d:
                        self.direction = 1
                    matrix[self.y][self.x].append(Object(
                        self.x,
                        self.y,
                        self.direction,
                        self.name,
                        self.text,
                        self.movement_state + 1
                    ))
                    return True
                return False
            for rule in level_rules:
                if f'{self.name} is stop' in rule.text_rule and status_push == 'push' and not self.text:
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
                        self.movement_state + 1
                    ))
                    return True
            if status_push is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.text):
                for i in range(len(matrix[self.y][self.x])):
                    if matrix[self.y][self.x][i].name == self.name:
                        matrix[self.y][self.x].pop(i)
                self.status_of_rotate = 0
                self.x += 1
                self.xpx += 50
                if not flag_3d:
                    self.direction = 1
                matrix[self.y][self.x].append(Object(
                    self.x,
                    self.y,
                    self.direction,
                    self.name,
                    self.text,
                    self.movement_state + 1
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
