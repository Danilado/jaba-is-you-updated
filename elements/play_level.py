"""draw_matrix.py hopefully refactored by Gospodin"""

from copy import copy
from typing import List, Optional

import pygame

import classes.Rules as Rules
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.TextRule import TextRule
from classes.state import State
from elements.global_classes import sound_manager
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES, STICKY
from utils import my_deepcopy


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

        self.level_name_object_text = self.text_to_png(level_name)
        self.circle_radius = 650
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
            if neighbours[index] is None:
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

    def check_vertically(self, i, j):
        for first_object in self.matrix[i][j]:
            if first_object.is_noun and len(self.matrix) - i > 2:

                for operator in self.matrix[i + 1][j]:
                    if operator.is_operator and operator.name != 'and':

                        for second_object in self.matrix[i + 2][j]:
                            if second_object.is_noun:
                                return self.form_rule(first_object.name, operator.name, second_object.name)

                            elif second_object.name == 'not' and len(self.matrix) - i > 3:
                                for third_object in self.matrix[i + 3][j]:
                                    if third_object.is_noun or third_object.is_property:
                                        return self.form_rule(first_object.name, operator.name, second_object.name)

                    elif operator.name == 'and':
                        further_rule_number = self.check_vertically(i + 2, j)
                        if further_rule_number != 0:
                            rule = self.level_rules[further_rule_number - 1]
                            text = rule.text_rule.split()
                            text[0] = first_object.name
                            return self.form_rule(*text)

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
            if not letter == ' ':
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
                self.moved = True
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
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                for rule_object in self.matrix[i][j]:
                    if not rule_object.is_text:
                        is_hot = False
                        is_hide = False
                        locked_sides = []
                        for rule in self.level_rules:
                            # TODO: Replace Conditional with Polymorphism instead of if-elif-elif-elif-elif-elif-else...
                            # Working on it ....

                            if rule_object.name in rule.text_rule:

                                if f'{rule_object.name} is broken' in rule.text_rule:
                                    Rules.broken.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        rules=self.level_rules)

                                elif f'{rule_object.name} is return' in rule.text_rule:
                                    Rules.return_rule.apply(
                                        matrix=matrix,
                                        rule_object=rule_object)

                                elif f'{rule_object.name} is you' in rule.text_rule:
                                    Rules.you.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        events=events,
                                        level_rules=self.level_rules
                                    )

                                elif f'{rule_object.name} is chill' in rule.text_rule:
                                    Rules.chill.apply(
                                        matrix=matrix,
                                        rule_object=rule_object)

                                elif f'{rule_object.name} is boom' in rule.text_rule:
                                    Rules.boom.apply(
                                        matrix=matrix,
                                        rule_object=rule_object)

                                elif f'{rule_object.name} is auto' in rule.text_rule:
                                    Rules.auto.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        level_rules=self.level_rules)

                                elif f'{rule_object.name} is up' in rule.text_rule:
                                    Rules.direction.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        direction='up')

                                elif f'{rule_object.name} is right' in rule.text_rule:
                                    Rules.direction.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        direction='right')

                                elif f'{rule_object.name} is down' in rule.text_rule:
                                    Rules.direction.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        direction='down')

                                elif f'{rule_object.name} is left' in rule.text_rule:
                                    Rules.direction.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        direction='left')

                                elif f'{rule_object.name} is fall' in rule.text_rule:
                                    Rules.fall.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        level_rules=self.level_rules)

                                elif f'{rule_object.name} is hide' in rule.text_rule:
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

                                elif f'{rule_object.name} is more' in rule.text_rule:
                                    Rules.more.apply(
                                        matrix=matrix,
                                        rule_object=rule_object,
                                        level_rules=self.level_rules)

                            rule_object.is_hot = is_hot
                            rule_object.is_hide = is_hide
                            rule_object.locked_sides = my_deepcopy(
                                locked_sides)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        if len(self.history_of_matrix) == 0:
            self.history_of_matrix.append(self.matrix)
        self.screen.fill("black")
        self.state = None

        self.functional_event_check(events)

        copy_matrix = self.copy_matrix(self.matrix)

        self.apply_rules(events, copy_matrix)

        if self.matrix != copy_matrix:
            self.history_of_matrix.append(self.copy_matrix(self.matrix))
            self.matrix = self.copy_matrix(copy_matrix)

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

        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    if self.first_iteration or self.moved:
                        if game_object.name in STICKY and not game_object.is_text:
                            neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.neighbours = neighbours
                            game_object.animation_init()
                    game_object.draw(self.screen)

        if self.first_iteration:
            self.first_iteration = False
        if self.moved:
            self.moved = False

        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)
        self.level_rules = self.remove_copied_rules(self.level_rules)

        self.level_start_animation()

        if self.state is None:
            self.state = State(GameState.flip, None)
        return self.state
