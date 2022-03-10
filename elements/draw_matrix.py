from typing import List, Optional

import pygame

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.rule import Rule
from classes.state import State
from elements.global_classes import sound_manager
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES, STICKY


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
        self.matrix: List[List[List[Object]]] = [[[]
                                                  for _ in range(32)] for _ in range(18)]
        self.parse_file(level_name)
        self.level_rules = []
        self.empty_object = Object(-1, -1, 0, 'empty', False)
        self.first_iteration = True
        self.moved = False
        self.circle_radius = 700
        self.delay = pygame.time.get_ticks()
        self.text_size = 0
        self.level_name = level_name

    def parse_file(self, level_name: str):
        """
        Парсинг уровней. Добавляет объекты в :attr:`~.Draw.matrix`.

        .. note::
            Если вы хотите перезаписать карту, не забудьте удалить объекты из :attr:`~.Draw.matrix`

        :param level_name: Название уровня в папке levels
        :raises OSError: Если какая либо проблема с открытием файла.
        """
        with open(f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420', 'r') as level_file:
            for line in level_file.readlines():
                parameters = line.strip().split(' ')
                if len(parameters) > 1:
                    self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                        int(parameters[0]),
                        int(parameters[1]),
                        int(parameters[2]),
                        parameters[3],
                        parameters[4].lower() == 'true'
                    ))

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
        offsets = [
            (0, -1),
            (1,  0),
            (0,  1),
            (-1, 0),
        ]
        neighbours = [None for _ in range(4)]
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

    def anime(self):
        if self.circle_radius > 0:
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 0), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (600, 0), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1000, 0), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1600, 0), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 900), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (300, 900), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (800, 900), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1200, 900), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 300), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 600), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1600, 100), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1600, 500), self.circle_radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (1600, 900), self.circle_radius)
            font = pygame.font.SysFont('segoeuisemibold', self.text_size)
            img = font.render('LEVEL {}'.format(self.level_name.split(".")[0]), True, (255, 255, 255))
            self.screen.blit(img, (600, 400))
            self.text_size += 1
            if pygame.time.get_ticks() - self.delay > 2000:
                self.circle_radius -= 8
                self.text_size -= 4

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
                    if self.first_iteration or self.moved:
                        if game_object.name in STICKY and not game_object.text:
                            neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.neighbours = neighbours
                            game_object.animation_init()
                    game_object.draw(self.screen)

        if self.first_iteration:
            self.first_iteration = False
        if self.moved:
            self.moved = False

        self.anime()

        if state is None:
            state = State(GameState.flip, None)

        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)

        return state
