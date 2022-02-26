from typing import List, Optional
from functools import partial

import pygame
import glob, os

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES
from classes.objects import Object
from elements.global_classes import GuiSettings
from classes.rule import Rule


class Draw(GameStrategy):
    def __init__(self, levelname: str, screen: SURFACE):
        super().__init__(screen)
        self.matrix: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.parse_file(levelname)
        self.level_rules = []

    def parse_file(self, levelname: str):
        leve_file = open(f'./levels/{levelname}.omegapog_map_file_type_MLG_1337_228_100500_69_420', 'r')
        lines = leve_file.read().split('\n')
        for line in lines:
            parameters = line.split(' ')
            if len(parameters) > 1:
                self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                    int(parameters[0]),
                    int(parameters[1]),
                    int(parameters[2]),
                    parameters[3],
                    False if parameters[4] == 'False' else True
                ))

    def obj_is_noun(self, obj: Object):
        return obj.name not in OPERATORS and ((obj.name in NOUNS and obj.text) or obj.name in PROPERTIES)

    def check_horizontally(self, i, j):
        for first_object in self.matrix[i][j]:
            if self.obj_is_noun(first_object) and len(self.matrix[i]) - j > 2:
                for operator in self.matrix[i][j + 1]:
                    if operator.name in OPERATORS and (operator.name != 'and'):
                        for second_object in self.matrix[i][j + 2]:
                            if self.obj_is_noun(second_object):
                                self.level_rules.append(
                                    Rule(f'{first_object.name} {operator.name} {second_object.name}',
                                         [first_object, operator, second_object]))
                                return len(self.level_rules)
                            elif second_object.name == 'not' and len(self.matrix[i]) - j > 3:
                                for third_object in self.matrix[i][j + 3]:
                                    if self.obj_is_noun(third_object):
                                        self.level_rules.append(
                                            Rule(
                                                f'{first_object.name} {operator.name} {second_object.name} {third_object.name}',
                                                [first_object, operator, second_object, third_object]))
                                        return len(self.level_rules)

                    elif operator.name == 'and':
                        a = self.check_horizontally(i, j + 2)
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
                                Rule(text_of_rule, objects))
                            return len(self.level_rules)

        return 0

    def check_vertically(self, i, j):
        for first_object in self.matrix[i][j]:
            if self.obj_is_noun(first_object) and len(self.matrix) - i > 2:
                for operator in self.matrix[i + 1][j]:
                    if operator.name in OPERATORS and operator.name != 'and':
                        for second_object in self.matrix[i + 2][j]:
                            if self.obj_is_noun(second_object):
                                self.level_rules.append(
                                    Rule(f'{first_object.name} {operator.name} {second_object.name}',
                                         [first_object, operator, second_object]))
                                return len(self.level_rules)
                            elif second_object.name == 'not' and len(self.matrix) - i > 3:
                                for third_object in self.matrix[i + 3][j]:
                                    if self.obj_is_noun(third_object):
                                        self.level_rules.append(
                                            Rule(
                                                f'{first_object.name} {operator.name} {second_object.name} {third_object.name}',
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
                                Rule(text_of_rule, objects))
                            return len(self.level_rules)
        return 0

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        self.screen.fill("black")
        self._state = None
        for event in events:
            if event.type == pygame.QUIT:
                self._state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._state = State(GameState.back)

        if SHOW_GRID:
            for x in range(0, RESOLUTION[0], 50):
                for y in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 50, 50), 1)

        for line in self.matrix:
            for cell in line:
                for object in cell:
                    object.draw(self.screen)

        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)

        if self._state is None:
            self._state = State(GameState.flip, None)
        return self._state
