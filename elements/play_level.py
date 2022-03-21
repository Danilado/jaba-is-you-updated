"""draw_matrix.py hopefully refactored by Gospodin"""

from utils import my_deepcopy
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES, STICKY
from global_types import SURFACE
from elements.global_classes import sound_manager
from classes.state import State
from classes.TextRule import TextRule
from classes.objects import Object
from classes.game_strategy import GameStrategy
from classes.game_state import GameState
import classes.Rules as Rules
import pygame
from typing import List, Optional
from sqlite3 import Timestamp
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

        self.level_name_object_text = self.text_to_png(level_name)
        self.circle_radius = 650

        self.delay = pygame.time.get_ticks()
        self.small_matrix_change = False
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

        with open(path_to_file, 'r') as level_file:
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

        offsets = [(0, -1), (1,  0), (0,  1), (-1, 0)]
        neighbours = [[] for _ in range(4)]

        if x == 0:
            neighbours[0] = [self.empty_object]
        elif x == RESOLUTION[1]//50-1:
            neighbours[2] = [self.empty_object]

        if y == 0:
            neighbours[3] = [self.empty_object]
        elif y == RESOLUTION[0]//50-1:
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
        for object in other_objects:
            rule_string += f' {object}'
        self.level_rules.append(TextRule(
            rule_string,
            [first_object, operator_object, *other_objects]
        ))
        return len(self.level_rules)

    def check_horizontally(self, i, j):
        for first_object in self.matrix[i][j]:
            if first_object.is_noun and len(self.matrix[i]) - j > 2:

                for operator in self.matrix[i][j + 1]:
                    if operator.is_operator and (operator.name != 'and'):

                        for second_object in self.matrix[i][j + 2]:
                            if second_object.is_noun or second_object.is_property:
                                return self.form_rule(first_object.name, operator.name, second_object.name)

                            elif second_object.name == 'not' and len(self.matrix[i]) - j > 3:
                                for third_object in self.matrix[i][j + 3]:
                                    if third_object.is_noun or third_object.is_property:
                                        return self.form_rule(first_object.name, operator.name, second_object.name, third_object.name)

                    elif operator.name == 'and':
                        further_rule_number = self.check_horizontally(i, j + 2)
                        if further_rule_number != 0:
                            rule = self.level_rules[further_rule_number - 1]
                            text = rule.text_rule.split()
                            text[0] = first_object.name
                            return self.form_rule(*text)

        return 0

    @staticmethod
    def obj_is_noun(obj: Object):
        return obj.name not in OPERATORS and obj.name in NOUNS and obj.is_text

    def check_vertically(self, i, j):
        for first_object in self.matrix[i][j]:
            if first_object.is_noun and len(self.matrix) - i > 2:
                for operator in self.matrix[i + 1][j]:
                    if operator.name in OPERATORS and operator.name != 'and':
                        for second_object in self.matrix[i + 2][j]:
                            if second_object.is_noun or second_object.name in PROPERTIES:
                                self.level_rules.append(
                                    TextRule(f'{first_object.name} {operator.name} {second_object.name}',
                                             [first_object, operator, second_object]))
                                return len(self.level_rules)
                            elif second_object.name == 'not' and len(self.matrix) - i > 3:
                                for third_object in self.matrix[i + 3][j]:
                                    if third_object.is_noun or third_object.name in PROPERTIES:
                                        self.level_rules.append(
                                            TextRule(
                                                f'{first_object.name} {operator.name} {second_object.name} '
                                                f'{third_object.name}',
                                                [first_object, operator, second_object, third_object]))
                                        return len(self.level_rules)
                    elif operator.name == 'and':
                        a = self.check_horizontally(i + 2, j)
                        if a != 0:
                            rule = self.level_rules[a - 1]
                            text = rule.text_rule.split()
                            objects = rule.objects_in_rule
                            objects[0] = first_object
                            text[0] = first_object.name
                            text_of_rule = ''
                            for words in text:
                                text_of_rule += f'{words} '
                            text_of_rule = text_of_rule[:-1]
                            self.level_rules.append(
                                TextRule(text_of_rule, objects))
                            return len(self.level_rules)
        return 0

    @staticmethod
    def copy_matrix(matrix):
        copy_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for obj in matrix[i][j]:
                    copy_matrix[i][j].append(copy(obj))

        return copy_matrix

    def music(self):
        # TODO by Gospodin: add music and theme choice in editor
        sound_manager.load_music("sounds/Music/ruin")

    @staticmethod
    def text_to_png(level_name):
        x_offset = 12
        level_text = 'level ' + level_name
        text_in_objects = []

        for letter in level_text:
            if letter not in [' ', '_', '-']:
                a = Object(x_offset, 6, 1, letter, True)
                text_in_objects.append(a)
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
                self.state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = State(GameState.back)
                if event.key == pygame.K_z:
                    self.status_cancel = True
                    self.moved = True
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                 pygame.K_d, pygame.K_SPACE, pygame.K_UP,
                                 pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
                    self.moved = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.status_cancel = False
                    self.moved = True

    def apply_rules(self, events: List[pygame.event.Event], matrix):
        Rules.processor.update_lists(matrix=matrix,
                                     events=events,
                                     level_rules=self.level_rules,
                                     objects_for_tp=self.objects_for_tp,
                                     state=self.state)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                for rule_object in self.matrix[i][j]:
                    #for i in range(len(self.matrix) - 1, -1, -1))
                    #for i in range(0, len(self.matrix), 1)
                    if not rule_object.special_text:
                        is_hot = False
                        is_hide = False
                        is_safe = False
                        locked_sides = []
                        is_open = False
                        is_shut = False
                        is_phantom = False

                        for rule in self.level_rules:
                            if f'{rule_object.name} is hide' in rule.text_rule:
                                is_hide = True

                            elif f'{rule_object.name} is hot' in rule.text_rule:
                                is_hot = True

                            elif f'{rule_object.name} is locked' in rule.text_rule:
                                if f'{rule_object.name} is lockeddown' in rule.text_rule:
                                    locked_sides.append('down')
                                elif f'{rule_object.name} is lockedup' in rule.text_rule:
                                    locked_sides.append('up')
                                elif f'{rule_object.name} is lockedleft' in rule.text_rule:
                                    locked_sides.append('left')
                                elif f'{rule_object.name} is lockedright' in rule.text_rule:
                                    locked_sides.append('right')

                            elif f'{rule_object.name} is melt' in rule.text_rule:
                                if rule_object.is_hot:
                                    matrix[i][j].remove(rule_object)
                                else:
                                    for object in matrix[i][j]:
                                        if object.is_hot:
                                            matrix[i][j].remove(
                                                rule_object)

                            elif f'{rule_object.name} is safe' in rule.text_rule:
                                rule_object.is_safe = True
                                is_safe = True

                            elif f'{rule_object.name} is win' in rule.text_rule:
                                for object in matrix[i][j]:
                                    for second_rule in self.level_rules:
                                        if f'{object.name} is you' in second_rule.text_rule:
                                            self.state = State(GameState.back)

                            elif f'{rule_object.name} is open' in rule.text_rule:
                                rule_object.is_open = is_open
                                is_open = True

                            elif f'{rule_object.name} is phantom' in rule.text_rule:
                                rule_object.is_phantom = is_phantom
                                is_phantom = True

                            elif f'{rule_object.name} is shut' in rule.text_rule:
                                rule_object.is_shut = is_shut
                                is_shut = True

                        rule_object.is_hot = is_hot
                        rule_object.is_hide = is_hide
                        rule_object.is_safe = is_safe
                        rule_object.locked_sides = my_deepcopy(
                            locked_sides)
                        rule_object.is_open = is_open
                        rule_object.is_shut = is_shut
                        rule_object.is_phantom = is_phantom

                        for rule in self.level_rules:

                            if rule_object.name in rule.text_rule:
                                Rules.processor.update_object(rule_object)
                                Rules.processor.process(rule.text_rule)

    def find_rules(self):
        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)
        self.level_rules = self.remove_copied_rules(
            self.level_rules)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        self.screen.fill("black")
        self.state = None

        self.functional_event_check(events)

        if self.status_cancel:
            if len(self.history_of_matrix) > 0:
                self.matrix = self.copy_matrix(self.history_of_matrix[-1])
                self.history_of_matrix.pop()
            else:
                self.matrix = self.copy_matrix(self.start_matrix)

        if SHOW_GRID:
            for x in range(0, RESOLUTION[0], 50):
                for y in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255), (x, y, 50, 50), 1)
        if self.moved:
            copy_matrix = self.copy_matrix(self.matrix)
            self.apply_rules(events, copy_matrix)
            if self.matrix != copy_matrix or self.small_matrix_change:
                self.history_of_matrix.append(self.copy_matrix(self.matrix))
                self.matrix = copy_matrix

            self.find_rules()
        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    if self.first_iteration or self.moved:
                        if game_object.name in STICKY and not game_object.is_text:
                            game_object.neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.animation = game_object.animation_init()
                    game_object.draw(self.screen)

        if self.first_iteration:
            self.find_rules()
            self.first_iteration = False

        if self.moved:
            self.moved = False

        if self.small_matrix_change:
            self.small_matrix_change = False

        #self.level_start_animation() if self.circle_radius > 0 else ...

        if self.state is None:
            self.state = State(GameState.flip, None)
        return self.state
