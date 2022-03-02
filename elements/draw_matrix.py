from typing import List, Optional

import pygame

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.rule import Rule
from classes.state import State
from elements.global_classes import sound_manager
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES


class Draw(GameStrategy):
    """
    Стратегия отрисовки уровня.

    :ivar matrix: Список списков списка объектов. То есть, карта объектов в игре.
    :ivar screen: Экран на котором будет происходить вся отрисовка.
    """

    def music(self):
        sound_manager.load_music("sounds/Music/ruin")

    def __init__(self, level_name: str, screen: SURFACE):
        super().__init__(screen)
        self.matrix: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.parse_file(level_name)
        self.level_rules = []

    def parse_file(self, level_name: str):
        """
        Парсинг уровней. Добавляет объекты в :attr:`~.Draw.matrix`.

        .. note::
            Если вы хотите перезаписать карту, не забудьте удалить объекты из :attr:`~.Draw.matrix`

        :param level_name: Название уровня в папке levels
        :raises OSError: Если какая либо проблема с открытием файла.
        """
        with open(f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420', 'r') as leve_file:
            for line in leve_file.readlines():
                parameters = line.strip().split(' ')
                if len(parameters) > 1:
                    self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                        int(parameters[0]),
                        int(parameters[1]),
                        int(parameters[2]),
                        parameters[3],
                        parameters[4].lower() == 'true'
                    ))

    @staticmethod
    def obj_is_noun(obj: Object):
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
                                                f'{first_object.name} {operator.name} {second_object.name} '
                                                f'{third_object.name}',
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
                                Rule(text_of_rule, objects))
                            return len(self.level_rules)
        return 0

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        self.screen.fill("black")
        state = None
        for event in events:
            if event.type == pygame.QUIT:
                state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = State(GameState.back)

        if SHOW_GRID:
            for x in range(0, RESOLUTION[0], 50):
                for y in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255), (x, y, 50, 50), 1)

        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    game_object.draw(self.screen)

        if state is None:
            state = State(GameState.flip, None)

        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)

        return state
