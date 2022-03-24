"""Модуль класса объекта"""
from copy import copy
import os
import os.path
from typing import List, Literal

import pygame

from elements.global_classes import sprite_manager
from global_types import SURFACE
from settings import TEXT_ONLY, SPRITE_ONLY, RESOLUTION, NOUNS, OPERATORS, PROPERTIES
from classes.animation import Animation
from classes.game_state import GameState
from classes.state import State

pygame.font.init()
font = pygame.font.Font("fonts/ConsolateElf.ttf", 15)


# TODO by quswadress
# Too many fields, refactor this please!

# Gospodin:
# Отнюдь. Слишком во многих файлах объекты и их поля
# вызываются без определения переменной как Object
# в циклых это вообще сделать, наверное, невозможно.
# Это значит, что
# Во первых, изменится половина кода
# Во вторых, придётся искать все упоминания объектов вручную
# В третьих, сами структуры выглядят по уродски, а иначе нужно
# Создавать классы, которые трудно сериализировать

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

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty",
                 is_text: bool = True, movement_state: int = 0, neighbours=None,
                 turning_side: Literal[0, 1, 2, 3, -1] = -1, animation=None,
                 safe=False, angle_3d: int = 90, is_3d=False, moved=False,
                 num_3d: int = 0):

        self.status = ''
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

        self.angle_3d = angle_3d
        self.num_3d = num_3d

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
        self.is_still = False
        self.is_sleep = False
        self.is_weak = False
        self.is_float = False
        self.is_3d = is_3d
        self.level_processor = None
        self.is_fall = False

        self.moved = moved
        self.recursively_used = False

        if self.name != 'empty' and self.animation is None:
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
                if not object.is_text and object.name == self.name and char_dict[index] not in key:
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
                    f"{self.name} fucked up while searching for files. Probably folder is corrupt \
                    or does not exist. This shouldn't happen in any circumstances")
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
        Метод отрисовки объекта
        """
        if not self.is_hide:
            self.animation.update()
            self.animation.draw(screen)

    def unparse(self) -> str:
        """Сериализовать объект в строку"""
        return f'{self.x} {self.y} {self.direction} {self.name} {self.is_text}'

    def get_index(self, matrix) -> int:
        """Ищет индекс объекта в клетке матрицы для удаления
        (костыль от Vlastelin)

        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :return: Индекс объекта в клетке массива
        :rtype: int
        """
        for i in range(len(matrix[self.y][self.x])):
            if matrix[self.y][self.x][i].name == self.name:
                return i
        return -1

    def move(self, matrix, level_rules, level_processor) -> None:
        """Выбор метода движения (2Д или 3Д)

        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]_
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param level_processor: Объект класса игры, в котором
        движется объект
        :type level_processor: PlayLevel
        """
        if self.is_3d:
            self.move_3d(matrix, level_rules, level_processor)
        else:
            self.move_2d(matrix, level_rules, level_processor)

    def move_2d(self, matrix, level_rules, level_processor) -> None:
        """Метод движения объекта в 2Д

        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param level_processor: Объект класса игры, в котором
        движется объект
        :type level_processor: PlayLevel"""
        self.level_processor = level_processor

        if self.turning_side == 0:
            self.moved = self.motion(1, 0, matrix, level_rules)
            self.direction = 1
        elif self.turning_side == 1:
            self.moved = self.motion(0, -1, matrix, level_rules)
            self.direction = 0
        elif self.turning_side == 2:
            self.moved = self.motion(-1, 0, matrix, level_rules)
            self.direction = 3
        elif self.turning_side == 3:
            self.moved = self.motion(0, 1, matrix, level_rules)
            self.direction = 2

    def move_3d(self, matrix, level_rules, level_processor) -> None:
        """Метод движения объекта в 3Д

        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param level_processor: Объект класса игры, в котором
        движется объект
        :type level_processor: PlayLevel
        """
        self.level_processor = level_processor
        if self.turning_side == 2:
            matrix[self.y][self.x].pop(self.get_index(matrix))
            self.angle_3d = (self.angle_3d - 90) % 360
            matrix[self.y][self.x].append(copy(self))
        elif self.turning_side == 0:
            matrix[self.y][self.x].pop(self.get_index(matrix))
            self.angle_3d = (self.angle_3d + 90) % 360
            matrix[self.y][self.x].append(copy(self))
        elif self.turning_side == 1:
            if self.angle_3d == 0:
                self.direction = 1
                self.motion(1, 0, matrix, level_rules)
            if self.angle_3d in (180, -180):
                self.direction = 3
                self.motion(-1, 0, matrix, level_rules)
            if self.angle_3d in (90, -270):
                self.direction = 2
                self.motion(0, 1, matrix, level_rules)
            if self.angle_3d in (-90, 270):
                self.direction = 0
                self.motion(0, -1, matrix, level_rules)
        elif self.turning_side == 3:
            pass

    @staticmethod
    def find_side(delta_x, delta_y) -> str:
        """Поиск направления движения

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :return: Сторона движения
        :rtype: str
        """
        side = None
        if delta_y > 0:
            side = 'down'
        elif delta_y < 0:
            side = 'up'
        if delta_x > 0:
            side = 'right'
        elif delta_x < 0:
            side = 'left'
        return side

    def update_parameters(self, delta_x, delta_y, matrix):
        """Обновление параметров объекта

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        """
        if not self.is_still:
            self.x += delta_x
            self.y += delta_y
            self.ypx -= delta_y * 50
            self.xpx -= delta_x * 50
        self.animation = None
        self.movement_state += 1
        self.moved = True
        side = self.find_side(delta_x, delta_y)
        if side == 'down':
            self.status_of_rotate = 3
            self.direction = 2
        elif side == 'up':
            self.status_of_rotate = 1
            self.direction = 0
        elif side == 'right':
            self.status_of_rotate = 0
            self.direction = 1
        elif side == 'left':
            self.status_of_rotate = 2
            self.direction = 3
        matrix[self.y][self.x].append(copy(self))

    def check_swap(self, delta_x, delta_y, matrix, level_rules, rule_object) -> True:
        """Проверяет правило swap у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может свапаться
        :type rule_object: Object
        :return: True\n"Так нужно" (c)Vlastelin
        :rtype: bool
        """
        for rule in level_rules:
            if f'{rule_object.name} is swap' in rule.text_rule or (
                    f'{self.name} is swap' in rule.text_rule and not self.is_phantom):
                matrix[self.y][self.x].pop(self.get_index(matrix))
                self.update_parameters(delta_x, delta_y, matrix)
                matrix[self.y][self.x].pop(rule_object.get_index(matrix))
                rule_object.update_parameters(-delta_x, -delta_y, matrix)
                return True
        return False

    def check_melt(self, delta_x, delta_y, matrix, level_rules, rule_object) -> bool:
        """Проверяет правило melt у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если объект выжил иначе False
        :rtype: bool
        """
        if not self.is_safe:
            for rule in level_rules:
                if f'{self.name} is melt' in rule.text_rule:
                    for sec_rule in level_rules:
                        if f'{rule_object.name} is hot' in sec_rule.text_rule:
                            matrix[self.y][self.x].pop(self.get_index(matrix))
                            return False
        for rule in level_rules:
            if self.is_hot and f'{rule_object.name} is melt' in rule.text_rule:
                matrix[self.y + delta_y][self.x +
                                         delta_x].pop(rule_object.get_index(matrix))
        return True

    def check_weak(self, delta_x, delta_y, matrix, level_rules, rule_object) -> bool:
        """Проверяет правило weak у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если объект выжил иначе False
        :rtype: bool
        """
        if not self.is_safe:
            for rule in level_rules:
                if f'{rule_object.name} is stop' in rule.text_rule and self.is_weak:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    return False
        for rule in level_rules:
            if f'{rule_object.name} is weak' in rule.text_rule:
                matrix[self.y + delta_y][self.x +
                                         delta_x].pop(rule_object.get_index(matrix))
        return True

    def check_shut_open(self, delta_x, delta_y, matrix, level_rules, rule_object) -> bool:
        """Проверяет правилa shut и open у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если объект выжил иначе False
        :rtype: bool
        """
        if not self.is_safe:
            for rule in level_rules:
                if self.is_open and f'{rule_object.name} is shut' in rule.text_rule \
                        or self.is_shut and f'{rule_object.name} is open' in rule.text_rule:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    matrix[self.y + delta_y][self.x +
                                             delta_x].pop(rule_object.get_index(matrix))
                    return False
        for rule in level_rules:
            if self.is_open and f'{rule_object.name} is shut' in rule.text_rule \
                    or self.is_shut and f'{rule_object.name} is open' in rule.text_rule:
                if not self.is_safe:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                matrix[self.y + delta_y][self.x +
                                         delta_x].pop(rule_object.get_index(matrix))
                if not self.is_safe:
                    return False

        return True

    def check_defeat(self, delta_x, delta_y, matrix, level_rules, rule_object) -> bool:
        """Проверяет правило defeat у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если объект выжил иначе False
        :rtype: bool
        """
        if not self.is_safe:
            for rule in level_rules:
                if f'{rule_object.name} is defeat' in rule.text_rule:
                    for sec_rule in level_rules:
                        if f'{self.name} is you' in sec_rule.text_rule:
                            matrix[self.y][self.x].pop(self.get_index(matrix))
                            return False

                        if f'{self.name} is 3d' in sec_rule.text_rule:
                            matrix[self.y][self.x].pop(self.get_index(matrix))
                            return False

        for rule in level_rules:
            if f'{self.name} is defeat' in rule.text_rule:
                for sec_rule in level_rules:
                    if f'{rule_object.name} is you' in sec_rule.text_rule:
                        matrix[self.y + delta_y][self.x +
                                                 delta_x].pop(rule_object.get_index(matrix))
                    elif f'{rule_object.name} is 3d' in sec_rule.text_rule:
                        matrix[self.y + delta_y][self.x +
                                                 delta_x].pop(rule_object.get_index(matrix))
        return True

    def check_sink(self, delta_x, delta_y, matrix, level_rules, rule_object) -> bool:
        """Проверяет правило sink у объекта и сразу
        выполняет действие, если возможно

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если объект выжил иначе False
        :rtype: bool
        """
        if not self.is_safe:
            for rule in level_rules:
                if f'{rule_object.name} is sink' in rule.text_rule:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    matrix[self.y + delta_y][self.x +
                                             delta_x].pop(rule_object.get_index(matrix))
                    return False
        for rule in level_rules:
            if f'{self.name} is sink' in rule.text_rule:
                matrix[self.y + delta_y][self.x +
                                         delta_x].pop(rule_object.get_index(matrix))
        return True

    def check_win(self, level_rules, rule_object) -> bool:
        """Проверяет правило win у объекта и сразу
        выполняет действие, если возможно. В случае победы
        возвращает игрока в предыдущее меню.

        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True если победа достигнута иначе False
        :rtype: bool
        """
        for rule in level_rules:
            if f'{rule_object.name} is win' in rule.text_rule:
                for sec_rule in level_rules:

                    if f'{self.name} is you' in sec_rule.text_rule:
                        self.level_processor.state = State(GameState.BACK)
                        return True

                    if f'{self.name} is 3d' in sec_rule.text_rule:
                        self.level_processor.state = State(GameState.BACK)
                        return True
        return False

    def check_rules(self, delta_x, delta_y, matrix, level_rules, rule_object) -> True:
        """Проверяет все правила, действующие на объект
        И меняет его статус в зависимости от них

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: True "Так нужно" (c)Vlastelin
        :rtype: bool
        """
        self.status = 'alive'
        if self.can_interact(rule_object, level_rules):
            self.check_win(level_rules, rule_object)

            if not self.check_melt(delta_x, delta_y, matrix, level_rules, rule_object) or \
                    not self.check_shut_open(delta_x, delta_y, matrix, level_rules, rule_object) or \
                    not self.check_defeat(delta_x, delta_y, matrix, level_rules, rule_object) or \
                    not self.check_sink(delta_x, delta_y, matrix, level_rules, rule_object) or \
                    not self.check_weak(delta_x, delta_y, matrix, level_rules, rule_object):
                self.status = 'dead'

            elif self.check_swap(delta_x, delta_y, matrix, level_rules, rule_object):
                self.status = 'moved_swap'

        return True

    def object_can_stop(self, rule_object, level_rules, with_push=False) -> bool:
        """Проверяет требуется ли обработка коллизий с объектом

        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :param with_push: Пытаются ли толкнуть объект
        :type with_push: bool
        :return: True если объект обрабатывает коллизии иначе False
        :rtype: bool
        """
        status = False
        for rule in level_rules:
            if f'{rule_object.name} is stop' in rule.text_rule or f'{rule_object.name} is pull' in rule.text_rule \
                    and self.can_interact(rule_object, level_rules):
                status = True
            if with_push:
                if f'{rule_object.name} is push' in rule.text_rule \
                        or rule_object.name in OPERATORS or rule_object.name in PROPERTIES \
                        or (rule_object.name in NOUNS and rule_object.is_text):
                    status = True
        return status

    def object_can_move(self, level_rules) -> bool:
        """Проверяет может ли звигаться объект в зависимости от правил
        !!! Такая интерпритация быстрее проверки через лист

        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :return: Может ли двигаться объект
        :rtype: bool
        """
        status = False
        moveable_rules_list = [
            f'{self.name} is move',
            f'{self.name} is push',
            f'{self.name} is auto',
            f'{self.name} is nudge',
            f'{self.name} is chill',
            f'{self.name} is you',
            f'{self.name} is fall',
            f'{self.name} is 3d',
        ]
        for rule in level_rules:
            if rule.text_rule in moveable_rules_list or \
               self.name in OPERATORS or self.name in PROPERTIES or (
                   self.name in NOUNS and self.is_text) and \
               self.check_valid_range(0, 0):
                status = True
        return status

    def check_valid_range(self, delta_x, delta_y) -> bool:
        """Проверяет выход за границы матрицы
        в процессе движения

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :return: Можно ли двигаться в данном направлении
        :rtype: bool
        """
        return RESOLUTION[0] // 50 - 1 >= self.x + delta_x >= 0 \
            and RESOLUTION[1] // 50 - 1 >= self.y + delta_y >= 0

    def pull_objects(self, delta_x, delta_y, matrix, level_rules) -> None:
        """Тянет объекты с правилом pull

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        """
        if self.check_valid_range(-delta_x, -delta_y):
            for rule_object in matrix[self.y - delta_y][self.x - delta_x]:
                if not rule_object.is_text and rule_object.name in NOUNS:
                    for rule in level_rules:
                        if f'{rule_object.name} is pull' in rule.text_rule:
                            rule_object.motion(
                                delta_x, delta_y, matrix, level_rules, 'pull')

    def check_locked(self, delta_x, delta_y) -> bool:
        """Блокирует стороны для движения в случае
        выхода за границы матрицы этим движением

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :return: Можно ли двигаться объекту в
        сторону его нынешнего движения
        :rtype: bool
        """
        side = self.find_side(delta_x, delta_y)
        if side == 'up' and self.y == 0:
            self.locked_sides.append('up')
        elif side == 'left' and self.x == 0:
            self.locked_sides.append('left')
        elif side == 'right' and self.x == RESOLUTION[0] // 50 - 1:
            self.locked_sides.append('right')
        elif side == 'down' and self.y == RESOLUTION[1] // 50 - 1:
            self.locked_sides.append('down')
        if side in self.locked_sides:
            return False
        return True

    def can_interact(self, rule_object, level_rules) -> bool:
        """Можно ли взаимодействовать с объектом
        (проверка на правило float)

        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param rule_object: Объект, с которым движущийся объект
        потенциально может взаимодействовать
        :type rule_object: Object
        :return: Может ли движущийся объект взаимодействовать с данным
        :rtype: bool
        """
        status_float_rule_object = False
        status_push_rule_object = False
        for rule in level_rules:
            if f'{rule_object.name} is float' in rule.text_rule \
                    and not (rule_object.name in OPERATORS or rule_object.name in PROPERTIES or (
                    rule_object.name in NOUNS and rule_object.is_text)):
                status_float_rule_object = True
            if f'{rule_object.name} is push' in rule.text_rule \
                    and not (rule_object.name in OPERATORS or rule_object.name in PROPERTIES or (
                    rule_object.name in NOUNS and rule_object.is_text)):
                status_push_rule_object = True
            if 'text is float' in rule.text_rule and self.is_text:
                self.is_float = True
        if self.is_float == status_float_rule_object \
                or rule_object.name in OPERATORS or rule_object.name in PROPERTIES or (
                rule_object.name in NOUNS and rule_object.is_text) or status_push_rule_object:
            return True
        return False

    def motion(self, delta_x, delta_y, matrix, level_rules, status=None) -> bool:
        """Осуществляет движение объекта

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :param matrix: Матрица, на которой расположен объект
        :type matrix: List[List[List[Object]]]
        :param level_rules: Правила уровня в момент движения
        :type level_rules: List[TextRule]
        :param status: статус объекта, defaults to None
        :type status: str, optional
        :return: Сдвинется ли объект
        :rtype: bool
        """
        if self.check_locked(delta_x, delta_y) and not self.is_sleep:
            for rule_object in matrix[self.y + delta_y][self.x + delta_x]:
                self.check_rules(delta_x, delta_y, matrix,
                                 level_rules, rule_object)
            if self.status == 'dead':
                return True
            if self.status == 'moved_swap':
                return False
            for rule_object in matrix[self.y + delta_y][self.x + delta_x]:
                if rule_object.object_can_stop(rule_object, level_rules) \
                        and self.can_interact(rule_object, level_rules):
                    return False
            status_motion = 'no collision'
            if self.status == 'alive':
                for rule_object in matrix[self.y + delta_y][self.x + delta_x]:
                    if (self.is_phantom or not rule_object.object_can_stop(rule_object, level_rules, True)
                            or not self.can_interact(rule_object, level_rules)) and status_motion != False:
                        if self.object_can_move(level_rules) and not self.is_still:
                            status_motion = True

                    elif self.is_fall:
                        status_motion = False

                    elif self.object_can_move(level_rules)\
                            and not self.is_still\
                            and status_motion != False:
                        if rule_object.motion(delta_x, delta_y, matrix, level_rules, 'push'):
                            status_motion = True
                        else:
                            status_motion = False

                if status_motion == True:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    self.pull_objects(delta_x, delta_y,
                                      matrix, level_rules)
                    self.update_parameters(delta_x, delta_y, matrix)
                    return True
                elif status_motion == False:
                    return False

            for rule in level_rules:
                if f'{self.name} is push' in rule.text_rule and status == 'push' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    self.update_parameters(delta_x, delta_y, matrix)
                    return True

            for rule in level_rules:
                if ((f'{self.name} is stop' in rule.text_rule and status == 'push')
                    or (f'{self.name} is pull' in rule.text_rule and status == 'push')) \
                        and not self.is_text:
                    return False

            if status is None or self.name in OPERATORS or self.name in PROPERTIES or (
                    self.name in NOUNS and self.is_text):
                matrix[self.y][self.x].pop(self.get_index(matrix))
                self.pull_objects(delta_x, delta_y, matrix, level_rules)
                self.update_parameters(delta_x, delta_y, matrix)

            for rule in level_rules:
                if f'{self.name} is pull' in rule.text_rule and status == 'pull' and not self.is_text:
                    matrix[self.y][self.x].pop(self.get_index(matrix))
                    self.pull_objects(delta_x, delta_y, matrix, level_rules)
                    self.update_parameters(delta_x, delta_y, matrix)

            return True
        return False

    def check_events(self, events: List[pygame.event.Event], number):
        """Метод обработки событий

        :param events: События, полученные при выхове
        :type events: List[pygame.event.Event]
        :param number: Номер правила YOU объекта (/YOU2)
        :type number: int
        """
        for event in events:
            if number == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.turning_side = 0
                    if event.key == pygame.K_w:
                        self.turning_side = 1
                    if event.key == pygame.K_a:
                        self.turning_side = 2
                    if event.key == pygame.K_s:
                        self.turning_side = 3
                    if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN,
                                     pygame.K_UP, pygame.K_SPACE]:
                        self.turning_side = -1
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                     pygame.K_d, pygame.K_SPACE]:
                        self.turning_side = -1
            if number == 2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.turning_side = 0
                    if event.key == pygame.K_UP:
                        self.turning_side = 1
                    if event.key == pygame.K_LEFT:
                        self.turning_side = 2
                    if event.key == pygame.K_DOWN:
                        self.turning_side = 3
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                     pygame.K_d, pygame.K_SPACE]:
                        self.turning_side = -1
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN,
                                     pygame.K_UP, pygame.K_SPACE]:
                        self.turning_side = -1

    @property
    def is_operator(self) -> bool:
        """Является ли объект оператором

        :return: Является ли объект оператором
        :rtype: bool
        """
        return self.name in OPERATORS

    @property
    def is_property(self) -> bool:
        """Является ли объект свойством

        :return: Является ли объект свойством
        :rtype: bool
        """
        return self.name in PROPERTIES

    @property
    def is_noun(self) -> bool:
        """Является ли объект существительным

        :return: Является ли объект существительным
        :rtype: bool
        """
        return self.name in NOUNS and self.name not in OPERATORS and self.is_text

    @property
    def special_text(self) -> bool:
        """Является ли объект текстом, но тут проперти особенный

        :return: Является ли объект текстом
        :rtype: bool
        """
        return self.is_text or self.name in TEXT_ONLY

    def __copy__(self):
        """Метод копирования объекта

        :return: Копия объекта
        :rtype: Object
        """
        copied_object = Object(
            x=self.x,
            y=self.y,
            direction=self.direction,
            name=self.name,
            is_text=self.is_text,
            movement_state=self.movement_state,
            neighbours=None,
            turning_side=self.turning_side,
            animation=self.animation,
            safe=self.is_safe,
            angle_3d=self.angle_3d,
            is_3d=self.is_3d,
            moved=self.moved,
            num_3d=self.num_3d

        )
        return copied_object
