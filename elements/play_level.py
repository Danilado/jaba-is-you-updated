"""draw_matrix.py hopefully refactored by Gospodin"""
import math

from utils import my_deepcopy
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES, STICKY, VERBS, INFIX, PREFIX, TEXT_ONLY, DEBUG
from global_types import SURFACE
from elements.global_classes import sound_manager
from classes.state import State
from classes.ray_casting import raycasting
from classes.text_rule import TextRule
from classes.objects import Object
from classes.game_strategy import GameStrategy
from classes.game_state import GameState
import classes.rules as rules
import pygame
from typing import List, Optional
from copy import copy


class PlayLevel(GameStrategy):
    def __init__(self, level_name: str, screen: SURFACE):
        super().__init__(screen)
        self.state = None

        self.matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        self.start_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        self.history_of_matrix = []

        self.parse_file(level_name)
        self.level_rules = []

        self.empty_object = Object(-1, -1, 0, 'empty', False)
        self.moved = False

        self.status_cancel = False
        self.first_iteration = True
        self.objects_for_tp = []

        self.num_obj_3d = 0
        self.count_3d_obj = 0
        self.flag = True

        self.level_name_object_text = self.text_to_png(level_name)
        self.circle_radius = 650

        self.delay = pygame.time.get_ticks()
        self.delay = pygame.time.get_ticks()

    def parse_file(self, level_name: str):
        """
        Парсинг уровней. Добавляет объекты в :attr:`~.Draw.matrix`.

        .. note::
            Если вы хотите перезаписать карту, не забудьте удалить объекты из :attr:`~.Draw.matrix`

        :param level_name: Название уровня в папке levels
        :raises OSError: Если какая либо проблема с открытием файла.
        """
        path_to_file = f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420'

        with open(path_to_file, mode='r', encoding='utf-8') as level_file:
            for line in level_file.readlines():
                parameters = line.strip().split(' ')

                if len(parameters) > 1:
                    x, y, direction, name = parameters[:-1]
                    self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                        int(x),
                        int(y),
                        int(direction),
                        name,
                        parameters[4].lower() == 'true'
                    ))

            self.start_matrix = self.matrix

    def get_neighbours(self, y, x) -> List:
        """Ищет соседей клетки сверху, справа, снизу и слева

        :param y: координата на матрице по оси y идёт первым,
        потому что ориентирование на матрице происходит зеркально относительно нормального
        :type y: int
        :param x: координата на матрице по оси x
        :type x: int
        :return: Массив с четырьмя клетками-соседями в порядке сверху, справа, снизу, слева
        :rtype: List[]
        """

        offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        neighbours = [[] for _ in range(4)]

        if x == 0:
            neighbours[0] = [self.empty_object]
        elif x == RESOLUTION[1] // 50 - 1:
            neighbours[2] = [self.empty_object]

        if y == 0:
            neighbours[3] = [self.empty_object]
        elif y == RESOLUTION[0] // 50 - 1:
            neighbours[1] = [self.empty_object]
        for index, offset in enumerate(offsets):
            if neighbours[index] == []:
                neighbours[index] = self.matrix[x + offset[1]][y + offset[0]]
        return neighbours

    @staticmethod
    def remove_copied_rules(arr):
        new_arr = []
        arr_text_rules = []
        for var in arr:
            if var.text_rule not in arr_text_rules:
                new_arr.append(var)
                arr_text_rules.append(var.text_rule)
        return new_arr

    def form_rule(self, first_object: Object, operator_object: Object, *other_objects: List[Object]):
        rule_string = f'{first_object} {operator_object}'
        for rule_object in other_objects:
            rule_string += f' {rule_object}'
        self.level_rules.append(TextRule(
            rule_string,
            [first_object, operator_object, *other_objects]
        ))
        return len(self.level_rules)

    @staticmethod
    def check_valid_range(x, y, delta_x, delta_y) -> bool:
        """Проверяет выход за границы матрицы
        в процессе движения

        :param delta_x: Сдвиг объекта по оси x
        :type delta_x: int
        :param delta_y: Сдвиг объекта по оси y
        :type delta_y: int
        :return: Можно ли двигаться в данном направлении
        :rtype: bool
        """
        return RESOLUTION[0] // 50 - 1 >= x + delta_x >= 0 \
               and RESOLUTION[1] // 50 - 1 >= y + delta_y >= 0

    def check_noun(self, i, j, delta_i, delta_j, status=None):
        noun_objects = []
        if self.check_valid_range(j, i, 0, 0):
            for first_object in self.matrix[i][j]:
                if first_object.is_noun:
                    cant_be_main = True
                    for second_object in self.matrix[i - delta_i][j - delta_j]:
                        if second_object.name in INFIX and status == 'main':
                            cant_be_main = False
                    if cant_be_main:
                        noun_objects.append([None, first_object])
                        if self.check_valid_range(j, i, delta_j * 2, delta_i * 2) and status == 'property':
                            for second_objects in self.matrix[i + delta_i][j + delta_j]:
                                if second_objects.name == 'and':
                                    nouns = self.check_noun(i + delta_i * 2, j + delta_j * 2, delta_i, delta_j,
                                                            'property')
                                    if not nouns:
                                        pass
                                    else:
                                        for noun in nouns:
                                            noun_objects.append(noun)
                        elif self.check_valid_range(j, i, delta_j * -2, delta_i * -2) and status == 'main':
                            status = None
                            for second_objects in self.matrix[i - delta_i][j - delta_j]:
                                if second_objects.name == 'and':
                                    status = 'and'
                                    nouns = self.check_noun(i + delta_i * -2, j + delta_j * -2, delta_i, delta_j,
                                                            'main')
                                    if not nouns:
                                        pass
                                    else:
                                        for noun in nouns:
                                            noun_objects.append(noun)
                            if status is None:
                                if not self.check_prefix(i - delta_i, j - delta_j, -delta_i, -delta_j):
                                    pass
                                else:
                                    prefix = self.check_prefix(i - delta_i, j - delta_j, -delta_i, -delta_j)
                                    noun_objects = []
                                    for pfix in prefix:
                                        noun_objects.append([pfix, first_object])
                                    last_i = prefix[-1].y
                                    last_j = prefix[-1].x
                                    for second_objects in self.matrix[last_i - delta_i][last_j - delta_j]:
                                        if second_objects.name == 'and':
                                            result = self.check_noun(last_i - delta_i * 2,
                                                                     last_j - delta_j * 2,
                                                                     delta_i, delta_j, 'main')
                                            if not result:
                                                pass
                                            else:
                                                nouns = result
                                                for noun in nouns:
                                                    noun_objects.append(noun)
                        return noun_objects
        return False

    def check_property(self, i, j, delta_i, delta_j):
        property_objects = []
        if self.check_valid_range(j, i, 0, 0):
            for first_object in self.matrix[i][j]:
                if first_object.name in PROPERTIES:
                    property_objects.append(['', first_object])
                    if self.check_valid_range(j, i, delta_j * 2, delta_i * 2):
                        for second_objects in self.matrix[i + delta_i][j + delta_j]:
                            if second_objects.name == 'and':
                                properties = self.check_property(i + delta_i * 2, j + delta_j * 2, delta_i, delta_j)
                                if not properties:
                                    pass
                                else:
                                    for property in properties:
                                        property_objects.append(['', property])
                    return property_objects
        return False

    def check_verb(self, i, j, delta_i, delta_j):
        if self.check_valid_range(j, i, 0, 0):
            for first_object in self.matrix[i][j]:
                if first_object.name in VERBS \
                        and self.check_valid_range(j, i, delta_j, delta_i):
                    object_not = None
                    if self.check_valid_range(j, i, delta_j, delta_i):
                        for maybe_not in self.matrix[i + delta_i][j + delta_j]:
                            if maybe_not.name == 'not':
                                delta_i *= 2
                                delta_j *= 2
                                object_not = maybe_not
                    nouns = self.check_noun(i + delta_i, j + delta_j, delta_i, delta_j, 'property')
                    if not nouns:
                        return False
                    else:
                        if object_not is None:
                            return [[first_object], nouns]
                        else:
                            return [[first_object], object_not, nouns]
                if first_object.name == 'is' \
                        and self.check_valid_range(j, i, delta_j, delta_i):
                    object_not = None
                    if self.check_valid_range(j, i, delta_j, delta_i):
                        for maybe_not in self.matrix[i + delta_i][j + delta_j]:
                            if maybe_not.name == 'not':
                                delta_i *= 2
                                delta_j *= 2
                                object_not = maybe_not

                    nouns = self.check_noun(i + delta_i, j + delta_j, delta_i, delta_j, 'property')
                    if not nouns:
                        properties = self.check_property(i + delta_i, j + delta_j, delta_i, delta_j)
                        if not properties:
                            return False
                        else:
                            if object_not is None:
                                return [[first_object], properties]
                            else:
                                return [[first_object], object_not, properties]
                    else:
                        if object_not is None:
                            return [[first_object], nouns]
                        else:
                            return [[first_object], object_not, nouns]
        return False

    def check_infix(self, i, j, delta_i, delta_j):
        if self.check_valid_range(j, i, 0, 0):
            for first_object in self.matrix[i][j]:
                if first_object.name in INFIX \
                        and self.check_valid_range(j, i, delta_j, delta_i):
                    nouns = self.check_noun(i + delta_i, j + delta_j, delta_i, delta_j)
                    if not nouns:
                        return False
                    else:
                        return [first_object, nouns[0][1]]
        return False

    def check_prefix(self, i, j, delta_i, delta_j):
        prefix_objects = []
        if self.check_valid_range(j, i, 0, 0):
            for first_object in self.matrix[i][j]:
                if first_object.name in PREFIX or first_object.name == 'not':
                    prefix_objects.append(first_object)
                    if self.check_valid_range(j, i, delta_j * -2, delta_i * -2):
                        for second_objects in self.matrix[i + delta_i][j + delta_j]:
                            if second_objects.name == 'and':
                                prefix = self.check_prefix(i + delta_i * 2, j + delta_j * 2, delta_i, delta_j)
                                if not prefix:
                                    pass
                                else:
                                    for pfix in prefix:
                                        prefix_objects.append(pfix)
                return prefix_objects
        return False

    def scan_rules(self, i, j, delta_i, delta_j):
        status = True
        verbs = []
        properties = []
        infix = []
        rules = []
        object_not = None
        nouns = self.check_noun(i, j, delta_i, delta_j, 'main')
        if not nouns:
            return False
        else:
            if not self.check_infix(i + delta_i, j + delta_j, delta_i, delta_j):
                arguments = self.check_verb(i + delta_i, j + delta_j, delta_i, delta_j)
                if not arguments:
                    status = False
                else:
                    if len(arguments) == 2:
                        verbs = arguments[0]
                        properties = arguments[1]
                    if len(arguments) == 3:
                        verbs = arguments[0]
                        object_not = arguments[1]
                        properties = arguments[2]
            else:
                infix = self.check_infix(i + delta_i, j + delta_j, delta_i, delta_j)
                arguments = self.check_verb(i + delta_i * 3, j + delta_j * 3, delta_i, delta_j)
                if not arguments:
                    status = False
                else:
                    if len(arguments) == 2:
                        verbs = arguments[0]
                        properties = arguments[1]
                    if len(arguments) == 3:
                        verbs = arguments[0]
                        object_not = arguments[1]
                        properties = arguments[2]

        if status:
            if len(infix) == 0:
                for noun in nouns:
                    for verb in verbs:
                        for property in properties:
                            if noun[0] is None:
                                if object_not is None:
                                    text = f'{noun[1].name} {verb.name} {property[1].name}'
                                    objects = [noun[1], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[1].name} {verb.name} {object_not.name} {property[1].name}'
                                    objects = [noun[1], verb, object_not, property]
                                    rules.append(TextRule(text, objects))
                            else:
                                if object_not is None:
                                    text = f'{noun[0].name} {noun[1].name} {verb.name} {property[1].name}'
                                    objects = [noun[0], noun[1], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[0].name} {noun[1].name} {verb.name} ' \
                                           f'{object_not.name} {property[1].name}'
                                    objects = [noun[0], noun[1], verb, object_not, property]
                                    rules.append(TextRule(text, objects))

            elif len(infix) != 0:
                for noun in nouns:
                    for verb in verbs:
                        for property in properties:
                            if noun[0] is None:
                                if object_not is None:
                                    text = f'{noun[1].name} {infix[0].name} {infix[1].name} {verb.name} {property.name}'
                                    objects = [noun[1], infix[1], infix[0], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[1].name} {infix[0].name} {infix[1].name}' \
                                           f' {verb.name} {object_not.name} {property.name}'
                                    objects = [noun[1], infix[1], infix[0], verb, object_not, property]
                                    rules.append(TextRule(text, objects))
                            else:
                                if object_not is None:
                                    text = f'{noun[0].name} {noun[1].name} {infix[0].name}' \
                                           f' {infix[1].name} {verb.name} {property.name}'
                                    objects = [noun[0], noun[1], infix[1], infix[0], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[0].name} {noun[1].name} {infix[0].name}' \
                                           f' {infix[1].name} {verb.name} {object_not.name} {property.name}'
                                    objects = [noun[0], noun[1], infix[1], infix[0], verb, object_not, property]
                                    rules.append(TextRule(text, objects))

            for rule in rules:
                self.level_rules.append(rule)

    @staticmethod
    def copy_matrix(matrix):
        copy_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for obj in matrix[i][j]:
                    copy_object = copy(obj)
                    copy_matrix[i][j].append(copy_object)

        return copy_matrix

    def music(self):
        # TODO by Gospodin: add music and theme choice in editor
        # Issue created.
        sound_manager.load_music("sounds/Music/ruin")

    @staticmethod
    def text_to_png(level_name):
        x_offset = 12
        level_text = 'level ' + level_name
        text_in_objects = []

        for letter in level_text:
            if letter not in [' ', '_', '-']:
                img_letter = Object(x_offset, 6, 1, letter, True)
                text_in_objects.append(img_letter)
            x_offset += 1

        return text_in_objects

    def level_start_animation(self):
        offsets = [(0, 0), (600, 0), (1000, 0), (1600, 0), (0, 900),
                   (300, 900), (800, 900), (1200, 900), (0, 300),
                   (0, 600), (1600, 100), (1600, 500), (1600, 900)]
        if self.circle_radius > 0:
            for offset in offsets:
                pygame.draw.circle(self.screen, (0, 50, 30),
                                   offset, self.circle_radius)
            if pygame.time.get_ticks() - self.delay <= 3000:
                for character_object in self.level_name_object_text:
                    character_object.draw(self.screen)
            if pygame.time.get_ticks() - self.delay > 3000:
                self.circle_radius -= 8

    def functional_event_check(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.state = State(GameState.BACK)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = State(GameState.BACK)
                if event.key == pygame.K_z:
                    self.status_cancel = True
                    self.moved = True
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                 pygame.K_d, pygame.K_SPACE, pygame.K_UP,
                                 pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
                    self.moved = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                 pygame.K_d, pygame.K_SPACE, pygame.K_UP,
                                 pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
                    self.moved = False
                if event.key == pygame.K_z:
                    self.status_cancel = False
                    self.moved = True

    def detect_iteration_direction(self, events: List[pygame.event.Event], matrix):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_SPACE, pygame.K_UP,
                                 pygame.K_LEFT]:
                    rules.processor.update_lists(level_processor=self,
                                                 matrix=matrix,
                                                 events=[event])
                    for i in range(len(self.matrix)):
                        for j in range(len(self.matrix[i])):
                            for rule_object in self.matrix[i][j]:
                                self.apply_rules(matrix, rule_object, i, j)
                elif event.key in [pygame.K_s, pygame.K_d, pygame.K_DOWN, pygame.K_RIGHT]:
                    rules.processor.update_lists(level_processor=self,
                                                 matrix=matrix,
                                                 events=[event])
                    for i in range(len(self.matrix) - 1, -1, -1):
                        for j in range(len(self.matrix[i]) - 1, -1, -1):
                            for rule_object in self.matrix[i][j]:
                                self.apply_rules(matrix, rule_object, i, j)

    def apply_rules(self, matrix, rule_object, i, j):
        if not rule_object.special_text:
            is_hot = False
            is_hide = False
            is_safe = False
            locked_sides = []
            is_open = False
            is_shut = False
            is_phantom = False
            is_text = False
            is_still = False
            is_sleep = False
            is_weak = False
            is_float = False
            is_3d = False
            is_fall = False
            for rule in self.level_rules:
                for noun in NOUNS:
                    if f'{rule_object.name} is {noun}' in rule.text_rule and not rule_object.is_text:
                        if rule_object.status_switch_name == 0:
                            matrix[i][j].pop(rule_object.get_index(matrix))
                            rule_object.name = noun
                            rule_object.status_switch_name = 1
                            matrix[i][j].append(copy(rule_object))
                        elif rule_object.status_switch_name == 1:
                            rule_object.status_switch_name = 2
                        elif rule_object.status_switch_name == 2:
                            rule_object.status_switch_name = 0




                if f'{rule_object.name} is 3d' in rule.text_rule:
                    is_3d = True

                elif f'{rule_object.name} is hide' in rule.text_rule:
                    is_hide = True

                elif f'{rule_object.name} is fall' in rule.text_rule:
                    is_fall = True

                elif f'{rule_object.name} is weak' in rule.text_rule:
                    is_weak = True

                elif f'{rule_object.name} is hot' in rule.text_rule:
                    is_hot = True

                elif f'{rule_object.name} is still' in rule.text_rule:
                    is_still = True

                elif f'{rule_object.name} is locked' in rule.text_rule:
                    if f'{rule_object.name} is lockeddown' in rule.text_rule:
                        locked_sides.append('down')
                    elif f'{rule_object.name} is lockedup' in rule.text_rule:
                        locked_sides.append('up')
                    elif f'{rule_object.name} is lockedleft' in rule.text_rule:
                        locked_sides.append('left')
                    elif f'{rule_object.name} is lockedright' in rule.text_rule:
                        locked_sides.append('right')

                elif f'{rule_object.name} is safe' in rule.text_rule:
                    is_safe = True

                elif f'{rule_object.name} is open' in rule.text_rule:
                    is_open = True

                elif f'{rule_object.name} is phantom' in rule.text_rule:
                    is_phantom = True

                elif f'{rule_object.name} is shut' in rule.text_rule:
                    is_shut = True

                elif f'{rule_object.name} is text' in rule.text_rule:
                    is_text = True

                elif f'{rule_object.name} is sleep' in rule.text_rule:
                    is_sleep = True

                elif f'{rule_object.name} is float' in rule.text_rule:
                    is_float = True

            rule_object.is_hot = is_hot
            rule_object.is_hide = is_hide
            rule_object.is_safe = is_safe
            rule_object.locked_sides = my_deepcopy(
                locked_sides)
            rule_object.is_open = is_open
            rule_object.is_shut = is_shut
            rule_object.is_phantom = is_phantom
            rule_object.is_text = is_text
            rule_object.is_still = is_still
            rule_object.is_sleep = is_sleep
            rule_object.is_weak = is_weak
            rule_object.is_float = is_float
            rule_object.is_3d = is_3d
            rule_object.is_fall = is_fall

            for rule in self.level_rules:

                if rule_object.name in rule.text_rule:
                    rules.processor.update_object(rule_object)
                    rules.processor.process(rule.text_rule)

            for rule in self.level_rules:
                if f'{rule_object.name} is win' in rule.text_rule \
                        and not rule_object.is_text:
                    for object in matrix[i][j]:
                        for second_rule in self.level_rules:
                            if f'{object.name} is you' in second_rule.text_rule:
                                self.state = State(GameState.BACK)

    def find_rules(self):
        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.scan_rules(i, j, 0, 1)
                self.scan_rules(i, j, 1, 0)
        self.level_rules = self.remove_copied_rules(
            self.level_rules)

    def update_sticky_neighbours(self, game_object: Object):
        game_object.neighbours = self.get_neighbours(
            game_object.x, game_object.y)
        game_object.recursively_used = True
        for neighbour_list in game_object.neighbours:
            for neighbour in neighbour_list:
                if not neighbour.recursively_used:
                    neighbour.recursively_used = True
                    self.update_sticky_neighbours(neighbour)
        game_object.animation = game_object.animation_init()
        game_object.moved = False

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        self.screen.fill("black")
        self.state = None
        level_3d = False
        count_3d_obj = 0

        self.functional_event_check(events)

        if self.status_cancel:
            if len(self.history_of_matrix) > 0:
                self.matrix = self.copy_matrix(self.history_of_matrix[-1])
                self.history_of_matrix.pop()
            else:
                self.matrix = self.copy_matrix(self.start_matrix)

        if self.moved:
            copy_matrix = self.copy_matrix(self.matrix)
            self.detect_iteration_direction(events, copy_matrix)
            self.history_of_matrix.append(self.copy_matrix(self.matrix))
            self.matrix = copy_matrix
            self.find_rules()

            if self.flag:
                for line in self.matrix:
                    for cell in line:
                        for game_object in cell:
                            if game_object.is_3d:
                                game_object.num_3d = self.count_3d_obj
                                self.count_3d_obj += 1
            self.flag = False

        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    if game_object.is_3d:
                        level_3d = True
                        if game_object.num_3d == self.num_obj_3d:
                            raycasting(self.screen, (game_object.xpx + 25, game_object.ypx + 25),
                                       game_object.angle_3d / 180 * math.pi, self.matrix)
                        count_3d_obj += 1

        if level_3d:
            if self.count_3d_obj != count_3d_obj:
                self.count_3d_obj = 0
                for line in self.matrix:
                    for cell in line:
                        for game_object in cell:
                            if game_object.is_3d:
                                game_object.num_3d = self.count_3d_obj
                                self.count_3d_obj += 1

            if count_3d_obj != 0:
                self.num_obj_3d %= self.count_3d_obj

        if not level_3d:
            for line in self.matrix:
                for cell in line:
                    for game_object in cell:
                        if self.first_iteration or self.moved:
                            if game_object.name in STICKY and not game_object.is_text and \
                                    (game_object.moved or self.first_iteration):
                                self.update_sticky_neighbours(game_object)
                        game_object.draw(self.screen)

            if SHOW_GRID:
                for x in range(0, RESOLUTION[0], 50):
                    for y in range(0, RESOLUTION[1], 50):
                        pygame.draw.rect(
                            self.screen, (255, 255, 255), (x, y, 50, 50), 1)

        if self.first_iteration:
            self.find_rules()
            self.first_iteration = False

        if self.circle_radius:
            self.level_start_animation()

        if self.moved:
            self.moved = False

        if self.state is None:
            self.state = State(GameState.FLIP, None)
        return self.state
