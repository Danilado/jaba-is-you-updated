"""draw_matrix.py hopefully refactored by Gospodin"""
import math
import time
from copy import copy
from random import randint
from typing import List, Optional, Dict, Tuple

import pygame

from classes import rules
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.particle import Particle, ParticleStrategy
from classes.ray_casting import raycasting
from classes.state import State
from classes.text_rule import TextRule
from elements.global_classes import sound_manager, palette_manager
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, PROPERTIES, STICKY, VERBS, INFIX, PREFIX, TEXT_ONLY, DEBUG
from utils import my_deepcopy


class PlayLevel(GameStrategy):
    def __init__(self, level_name: str, screen: SURFACE):
        super().__init__(screen)
        self.state: Optional[State] = None

        self.matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        self.start_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        self.history_of_matrix = []
        self.delta_cancel = 0

        self.parse_file(level_name)
        self.level_rules = []

        self.empty_object = Object(-1, -1, 0, 'empty',
                                   False, self.current_palette)
        self.moved = False

        self.status_cancel = False
        self.first_iteration = True
        self.objects_for_tp = []

        self.win_offsets = [[(775, 325), 0], [(825, 325), 0], [(725, 325), 0], [(875, 325), 0], [(675, 325), 0], [(925, 325), 0], [(625, 325), 0], [(975, 325), 0], [
            (575, 325), 0], [(1025, 325), 0], [(525, 325), 0], [(1075, 325), 0], [(475, 325), 0], [(1100, 325), 0], [(450, 325), 0], [(1125, 325), 0], [(425, 325), 0]]
        self.flag_to_win_animation = False
        self.flag_to_delay = False
        self.win_text = self.text_to_png('congratulations')

        self.num_obj_3d = 0
        self.count_3d_obj = 0
        self.flag = True

        self.move_delay = pygame.time.get_ticks()

        self.level_name_object_text = self.text_to_png('level ' + level_name)
        self.flag_to_level_start_animation = True
        self.circle_radius = 650

        self.delay = pygame.time.get_ticks()

        self.particles = [Particle(self.screen, 'dot', ParticleStrategy((randint(0, 1600), randint(-50, 1650)), (950, - 50), (randint(20, 35), randint(
            40, 65)), (randint(0, 360), randint(0, 360*5)), 20, 60 + randint(-20, 20), True, True), self.current_palette.pixels[3][6]) for _ in range(40)]

        self.apply_rules_cache: Dict[str, Object] = {}

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
            for line_index, line in enumerate(level_file.readlines()):
                parameters = line.strip().split(' ')

                if len(parameters) > 1 and line_index > 0:
                    x, y, direction, name = parameters[:-1]
                    self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                        int(x),
                        int(y),
                        int(direction),
                        name,
                        parameters[4].lower() == 'true',
                        self.current_palette
                    ))
                else:
                    self.current_palette = palette_manager.get_palette(
                        parameters[0])

            self.start_matrix = self.matrix
        if DEBUG:
            print("\n".join((
                "-"*100,
                f"Level {level_name} successfully parsed!",
                f"palette: {self.current_palette.name}",
                f"palette size: {len(self.current_palette.pixels[0])}x{len(self.current_palette.pixels)}"
            )))

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
            if not neighbours[index]:
                neighbours[index] = self.matrix[x + offset[1]][y + offset[0]]
        return neighbours

    @staticmethod
    def remove_copied_rules(arr):
        new_arr = []
        arr_text_rules = []
        for rule in arr:
            if rule.text_rule not in arr_text_rules:
                new_arr.append(rule)
                arr_text_rules.append(rule.text_rule)
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
        return RESOLUTION[0] // 50 - 1 >= x + delta_x >= 0 and RESOLUTION[1] // 50 - 1 >= y + delta_y >= 0

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
                                    if nouns:
                                        for noun in nouns:
                                            noun_objects.append(noun)
                        elif self.check_valid_range(j, i, delta_j * -2, delta_i * -2) and status == 'main':
                            status = None
                            for second_objects in self.matrix[i - delta_i][j - delta_j]:
                                if second_objects.name == 'and':
                                    status = 'and'
                                    nouns = self.check_noun(i + delta_i * -2, j + delta_j * -2, delta_i, delta_j,
                                                            'main')
                                    if nouns:
                                        for noun in nouns:
                                            noun_objects.append(noun)
                            if status is None:
                                if self.check_prefix(i - delta_i, j - delta_j, -delta_i, -delta_j):
                                    prefix = self.check_prefix(
                                        i - delta_i, j - delta_j, -delta_i, -delta_j)
                                    noun_objects = []
                                    for pfix in prefix:
                                        noun_objects.append(
                                            [pfix, first_object])
                                    last_i = prefix[-1].y
                                    last_j = prefix[-1].x
                                    for second_objects in self.matrix[last_i - delta_i][last_j - delta_j]:
                                        if second_objects.name == 'and':
                                            result = self.check_noun(last_i - delta_i * 2,
                                                                     last_j - delta_j * 2,
                                                                     delta_i, delta_j, 'main')
                                            if result:
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
                                properties = self.check_property(
                                    i + delta_i * 2, j + delta_j * 2, delta_i, delta_j)
                                if properties:
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
                    nouns = self.check_noun(
                        i + delta_i, j + delta_j, delta_i, delta_j, 'property')
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

                    nouns = self.check_noun(
                        i + delta_i, j + delta_j, delta_i, delta_j, 'property')
                    if not nouns:
                        properties = self.check_property(
                            i + delta_i, j + delta_j, delta_i, delta_j)
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
                    nouns = self.check_noun(
                        i + delta_i, j + delta_j, delta_i, delta_j)
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
                                prefix = self.check_prefix(
                                    i + delta_i * 2, j + delta_j * 2, delta_i, delta_j)
                                if isinstance(prefix, list):
                                    for prefix_object in prefix:
                                        prefix_objects.append(prefix_object)
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
                arguments = self.check_verb(
                    i + delta_i, j + delta_j, delta_i, delta_j)
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
                infix = self.check_infix(
                    i + delta_i, j + delta_j, delta_i, delta_j)
                arguments = self.check_verb(
                    i + delta_i * 3, j + delta_j * 3, delta_i, delta_j)
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
                                    objects = [noun[1], verb,
                                               object_not, property]
                                    rules.append(TextRule(text, objects))
                            else:
                                if object_not is None:
                                    text = f'{noun[0].name} {noun[1].name} {verb.name} {property[1].name}'
                                    objects = [
                                        noun[0], noun[1], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[0].name} {noun[1].name} {verb.name} ' \
                                           f'{object_not.name} {property[1].name}'
                                    objects = [noun[0], noun[1],
                                               verb, object_not, property]
                                    rules.append(TextRule(text, objects))

            elif len(infix) != 0:
                for noun in nouns:
                    for verb in verbs:
                        for property in properties:
                            if noun[0] is None:
                                if object_not is None:
                                    text = f'{noun[1].name} {infix[0].name} {infix[1].name} {verb.name} {property.name}'
                                    objects = [noun[1], infix[1],
                                               infix[0], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[1].name} {infix[0].name} {infix[1].name}' \
                                           f' {verb.name} {object_not.name} {property.name}'
                                    objects = [
                                        noun[1], infix[1], infix[0], verb, object_not, property]
                                    rules.append(TextRule(text, objects))
                            else:
                                if object_not is None:
                                    text = f'{noun[0].name} {noun[1].name} {infix[0].name}' \
                                           f' {infix[1].name} {verb.name} {property.name}'
                                    objects = [noun[0], noun[1],
                                               infix[1], infix[0], verb, property]
                                    rules.append(TextRule(text, objects))
                                else:
                                    text = f'{noun[0].name} {noun[1].name} {infix[0].name}' \
                                           f' {infix[1].name} {verb.name} {object_not.name} {property.name}'
                                    objects = [noun[0], noun[1], infix[1],
                                               infix[0], verb, object_not, property]
                                    rules.append(TextRule(text, objects))

            for rule in rules:
                self.level_rules.append(rule)

    @staticmethod
    def copy_matrix(matrix):
        copy_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]

        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for obj in cell:
                    copy_object = copy(obj)
                    copy_matrix[i][j].append(copy_object)

        return copy_matrix

    def on_init(self):
        # TODO by Gospodin: add music and theme choice in editor
        # Issue created.
        sound_manager.load_music("sounds/Music/ruin")

    def text_to_png(self, text):
        if len(text) >= 32:
            x_offset = 0
        else:
            x_offset = (32 - len(text)) // 2
        text_in_objects = []

        for letter in text:
            if letter in TEXT_ONLY:
                img_letter = Object(x_offset, 6, 1, letter,
                                    True, self.current_palette)
                text_in_objects.append(img_letter)
            x_offset += 1

        return text_in_objects

    def level_start_animation(self):
        offsets = [(0, 0), (600, 0), (1000, 0), (1600, 0), (0, 900),
                   (300, 900), (800, 900), (1200, 900), (0, 300),
                   (0, 600), (1600, 100), (1600, 500), (1600, 900)]
        for offset in offsets:
            pygame.draw.circle(self.screen, self.current_palette.pixels[3][6],
                               offset, self.circle_radius)
        if pygame.time.get_ticks() - self.delay <= 3000:
            for character_object in self.level_name_object_text:
                character_object.draw(self.screen)
        if pygame.time.get_ticks() - self.delay > 3000:
            self.circle_radius -= 8
        if self.circle_radius <= 0:
            self.circle_radius = 0
            self.flag_to_level_start_animation = False

    def win_animation(self):
        boarder_offsets = [(0, 0), (600, 0), (1000, 0), (1600, 0), (0, 900),
                           (300, 900), (800, 900), (1200, 900), (0, 300),
                           (0, 600), (1600, 100), (1600, 500), (1600, 900)]
        max_radius = 100
        if not self.flag_to_level_start_animation and self.flag_to_win_animation:
            for offset, radius in self.win_offsets:
                pygame.draw.circle(self.screen, self.current_palette.pixels[3][6],
                                   offset, radius)
            if self.win_offsets[0][1] < max_radius:
                self.win_offsets[0][1] += 0.1 * (len(self.win_offsets))
                for index in range(1, len(self.win_offsets), 2):
                    self.win_offsets[index][1] += 0.1 * \
                        (len(self.win_offsets) - index)
                    self.win_offsets[index + 1][1] += 0.1 * \
                        (len(self.win_offsets) - index)

            if self.win_offsets[0][1] >= max_radius and not self.flag_to_delay:
                self.flag_to_delay = True
                self.delay = pygame.time.get_ticks()

            if self.win_offsets[0][1] >= max_radius:
                for character_object in self.win_text:
                    character_object.draw(self.screen)

            if self.win_offsets[0][1] >= max_radius and pygame.time.get_ticks() - self.delay >= 1000:
                for offset1 in boarder_offsets:
                    pygame.draw.circle(
                        self.screen, self.current_palette.pixels[3][6], offset1, self.circle_radius)
                self.circle_radius += 8

            if self.circle_radius >= 650:
                self.state = State(GameState.BACK)

    def functional_event_check(self, events: List[pygame.event.Event]):
        flag = False
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
                    flag = 1
                    self.move_delay = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.status_cancel = False
                    self.moved = True

        if not flag:
            pressed = pygame.key.get_pressed()
            if pygame.time.get_ticks() - 200 > self.move_delay:
                self.move_delay = pygame.time.get_ticks()
                self.moved = any(pressed[key] for key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                                          pygame.K_d, pygame.K_SPACE, pygame.K_UP,
                                                          pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT])

    def detect_iteration_direction(self, events: List[pygame.event.Event], matrix):
        pressed = pygame.key.get_pressed()
        if any(pressed[key] for key in [pygame.K_w, pygame.K_a, pygame.K_SPACE, pygame.K_UP,
                                        pygame.K_LEFT]):
            rules.processor.update_lists(level_processor=self,
                                         matrix=matrix,
                                         events=events)
            for i, line in enumerate(self.matrix):
                for j, cell in enumerate(line):
                    for rule_object in cell:
                        self.apply_rules(matrix, rule_object, i, j)
        elif any(pressed[key] for key in [pygame.K_s, pygame.K_d, pygame.K_DOWN, pygame.K_RIGHT]):
            rules.processor.update_lists(level_processor=self,
                                         matrix=matrix,
                                         events=events)
            for i in range(len(self.matrix) - 1, -1, -1):
                for j in range(len(self.matrix[i]) - 1, -1, -1):
                    for rule_object in self.matrix[i][j]:
                        self.apply_rules(matrix, rule_object, i, j)

    def apply_rules(self, matrix, rule_object, i, j):
        if not rule_object.special_text:
            is_hot = is_hide = is_safe = is_open = is_shut = is_phantom = \
                is_text = is_still = is_sleep = is_weak = is_float = is_3d = is_fall = False
            locked_sides = []
            has_objects = []
            for rule in self.level_rules:
                for noun in NOUNS:
                    if f'{rule_object.name} is {noun}' == rule.text_rule and not rule_object.is_text:
                        if rule_object.status_switch_name == 0:
                            matrix[i][j].pop(rule_object.get_index(matrix))
                            rule_object.name = noun
                            rule_object.status_switch_name = 1
                            rule_object.animation = rule_object.animation_init()
                            matrix[i][j].append(copy(rule_object))
                        elif rule_object.status_switch_name == 1:
                            rule_object.status_switch_name = 2
                        elif rule_object.status_switch_name == 2:
                            rule_object.status_switch_name = 0
                    if f'{rule_object.name} has {noun}' in rule.text_rule and not rule_object.is_text:
                        has_objects.append(noun)

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
            rule_object.locked_sides = my_deepcopy(locked_sides)
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
            rule_object.has_objects = has_objects

            for rule in self.level_rules:
                if rule_object.name in rule.text_rule:
                    rules.processor.update_object(rule_object)
                    rules.processor.process(rule.text_rule)

    def find_rules(self):
        self.level_rules.clear()
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
        neighbour_list: List[Object]
        for neighbour_list in game_object.neighbours:
            for neighbour in neighbour_list:
                if not neighbour.recursively_used:
                    neighbour.recursively_used = True
                    self.update_sticky_neighbours(neighbour)
        game_object.animation = game_object.animation_init()
        game_object.moved = False

    def check_matrix(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                for obj in self.matrix[i][j]:
                    if obj.x != j or obj.y != i:
                        obj.x = j
                        obj.y = i
                        obj.animation = obj.animation_init()
                        self.matrix[i][j].pop(obj.get_index(self.matrix))
                        obj.animation = obj.animation_init()
                        self.matrix[i][j].append(copy(obj))
                        obj.animation = obj.animation_init()

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        self.screen.fill(self.current_palette.pixels[4][6])
        self.state = None
        level_3d = False
        count_3d_obj = 0

        for particle in self.particles:
            particle.draw(self.screen)

        self.functional_event_check(events)
        if self.status_cancel:
            new_time = pygame.time.get_ticks()
            if new_time > self.delta_cancel + 200:
                if len(self.history_of_matrix) > 0:
                    self.matrix = self.copy_matrix(self.history_of_matrix[-1])
                    self.history_of_matrix.pop()
                    self.check_matrix()
                    self.delta_cancel = new_time
                else:
                    self.matrix = self.copy_matrix(self.start_matrix)
                    self.check_matrix()
                    self.delta_cancel = new_time

        if self.moved and not self.flag_to_win_animation:
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

        # TODO by quswadress: И паттерн стратегия такой: Ну да, ну да, делайте свои большие if-ы, раздувайте классы!
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
        else:
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
            self.matrix = self.copy_matrix(self.start_matrix)
            self.first_iteration = False

        if self.flag_to_level_start_animation:
            self.level_start_animation()

        if self.flag_to_win_animation:
            self.win_animation()

        if self.moved:
            self.moved = False

        if self.state is None:
            self.state = State(GameState.FLIP, None)
        return self.state
