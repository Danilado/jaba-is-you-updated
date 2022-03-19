import warnings
import random
from typing import List, Optional

import pygame

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.ray_casting import RayCasting
from classes.rule import Rule
from settings import *
from classes.state import State
from elements.global_classes import sound_manager
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION, NOUNS, OPERATORS, PROPERTIES, STICKY
from utils import my_deepcopy


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
        self.anim_obj = self.words_to_png(level_name)
        self.parse_file(level_name)
        self.level_rules = []
        self.history_of_matrix = []
        self.status_cancel = False
        self.start_matrix: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        self.empty_object = Object(-1, -1, 0, 'empty', False)
        self.first_iteration = True
        self.moved = False
        self.circle_radius = 650
        self.delay = pygame.time.get_ticks()
        self.angle_3d = 90

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
                    if name == "jaba":
                        warnings.warn(f"Level {level_name} have old jaba/frog naming. Need to rename...")
                        name = "frog"
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
        offsets = [
            (0, -1),
            (1,  0),
            (0,  1),
            (-1, 0),
        ]
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
    def obj_is_noun(obj: Object):
        return obj.name not in OPERATORS and obj.name in NOUNS and obj.text

    @staticmethod
    def remove_copies_rules(arr):
        new_arr = []
        arr_text_rules = []
        for var in arr:
            if var.text_rule not in arr_text_rules:
                new_arr.append(var)
                arr_text_rules.append(var.text_rule)
        return new_arr

    def check_horizontally(self, i, j):
        for first_object in self.matrix[i][j]:
            if self.obj_is_noun(first_object) and len(self.matrix[i]) - j > 2:
                for operator in self.matrix[i][j + 1]:
                    if operator.name in OPERATORS and (operator.name != 'and'):
                        for second_object in self.matrix[i][j + 2]:
                            if self.obj_is_noun(second_object) or second_object.name in PROPERTIES:
                                self.level_rules.append(
                                    Rule(f'{first_object.name} {operator.name} {second_object.name}',
                                         [first_object, operator, second_object]))
                                return len(self.level_rules)
                            elif second_object.name == 'not' and len(self.matrix[i]) - j > 3:
                                for third_object in self.matrix[i][j + 3]:
                                    if self.obj_is_noun(third_object) or third_object.name in PROPERTIES:
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
                                    if self.obj_is_noun(third_object) or third_object.name in PROPERTIES:
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

    @staticmethod
    def copy_matrix(matrix):
        copy_matrix: List[List[List[Object]]] = [[[]
                                                  for _ in range(32)] for _ in range(18)]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for obj in matrix[i][j]:
                    copy_matrix[i][j].append(
                        Object(obj.x, obj.y, obj.direction, obj.name, obj.text))
                    # TODO: Add __copy__ to Object, and use it here
        return copy_matrix

    @staticmethod
    def words_to_png(level_count):
        x = 12
        level = 'level' + str(level_count)
        arr_obj = []
        for obj in level:
            a = Object(x, 6, 1, obj, True)
            arr_obj.append(a)
            x += 1
        return arr_obj

    def animation_level(self):
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
            if pygame.time.get_ticks() - self.delay <= 3000:
                for obj in self.anim_obj:
                    obj.draw(self.screen)
            if pygame.time.get_ticks() - self.delay > 3000:
                self.circle_radius -= 8

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        flag = False
        if len(self.history_of_matrix) == 0:
            self.history_of_matrix.append(self.matrix)
        self.screen.fill("black")
        state = None

        for event in events:
            if event.type == pygame.QUIT:
                state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                self.moved = True
                if event.key == pygame.K_ESCAPE:
                    state = State(GameState.back)
                if event.key == pygame.K_z:
                    self.status_cancel = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.status_cancel = False

        copy_matrix = my_deepcopy(self.matrix)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                for rule_object in self.matrix[i][j]:
                    if not rule_object.text:
                        is_hot = False
                        is_hide = False
                        locked_sides = []
                        for rule in self.level_rules:
                            if f'{rule_object.name} is 3d' in rule.text_rule:
                                flag = True
                                RayCasting(self.screen, (rule_object.xpx + 25, rule_object.ypx + 25),
                                           rule_object.angle_3d / 180 * math.pi, copy_matrix)
                            # TODO: Replace Conditional with Polymorphism instead of if-elif-elif-elif-elif-elif-else...
                            if f'{rule_object.name} is broken' in rule.text_rule:
                                for sec_rule in self.level_rules:
                                    if f'{rule_object.name}' in sec_rule.text_rule and \
                                            sec_rule.text_rule != f'{rule_object.name} is broken':
                                        self.level_rules.remove(sec_rule)

                            if f'{rule_object.name} is return' in rule.text_rule:
                                rule_object.direction += 1
                                rule_object.status_of_rotate += 1
                                if rule_object.direction > 3:
                                    rule_object.direction = 0
                                if rule_object.status_of_rotate > 3:
                                    rule_object.status_of_rotate = 0

                            if f'{rule_object.name} is you' in rule.text_rule:
                                rule_object.check_events(events)
                                rule_object.move(copy_matrix, self.level_rules, flag)

                            if f'{rule_object.name} is chill' in rule.text_rule:
                                rand_dir = random.randint(0, 5)
                                if rand_dir == 0:
                                    rule_object.move_up(
                                        copy_matrix, self.level_rules)
                                if rand_dir == 1:
                                    rule_object.move_right(
                                        copy_matrix, self.level_rules)
                                if rand_dir == 2:
                                    rule_object.move_down(
                                        copy_matrix, self.level_rules)
                                if rand_dir == 3:
                                    rule_object.move_left(
                                        copy_matrix, self.level_rules)

                            if f'{rule_object.name} is boom' in rule.text_rule:
                                copy_matrix[i][j].clear()

                            if f'{rule_object.name} is auto' in rule.text_rule:
                                if rule_object.direction == 0:
                                    rule_object.move_up(
                                        copy_matrix, self.level_rules)
                                if rule_object.direction == 1:
                                    rule_object.move_right(
                                        copy_matrix, self.level_rules)
                                if rule_object.direction == 2:
                                    rule_object.move_down(
                                        copy_matrix, self.level_rules)
                                if rule_object.direction == 3:
                                    rule_object.move_left(
                                        copy_matrix, self.level_rules)

                            if f'{rule_object.name} is up' in rule.text_rule:
                                rule_object.direction = 0
                                rule_object.status_of_rotate = 1

                            if f'{rule_object.name} is right' in rule.text_rule:
                                rule_object.direction = 1
                                rule_object.status_of_rotate = 0

                            if f'{rule_object.name} is down' in rule.text_rule:
                                rule_object.direction = 2
                                rule_object.status_of_rotate = 3

                            if f'{rule_object.name} is left' in rule.text_rule:
                                rule_object.direction = 3
                                rule_object.status_of_rotate = 2

                            if f'{rule_object.name} is fall' in rule.text_rule:
                                status_of_fall = True
                                while status_of_fall:
                                    status_of_fall = rule_object.move_down(
                                        copy_matrix, self.level_rules)

                            if f'{rule_object.name} is hide' in rule.text_rule:
                                is_hide = True

                            if f'{rule_object.name} is hot' in rule.text_rule:
                                is_hot = True

                            if f'{rule_object.name} is locked' in rule.text_rule:
                                if f'{rule_object.name} is lockeddown' in rule.text_rule:
                                    locked_sides.append('down')
                                if f'{rule_object.name} is lockedup' in rule.text_rule:
                                    locked_sides.append('up')
                                if f'{rule_object.name} is lockedleft' in rule.text_rule:
                                    locked_sides.append('left')
                                if f'{rule_object.name} is lockedright' in rule.text_rule:
                                    locked_sides.append('right')

                            if f'{rule_object.name} is melt' in rule.text_rule and rule_object.is_hot:
                                copy_matrix[i][j].remove(rule_object)

                            if f'{rule_object.name} is more' in rule.text_rule:
                                status_clone = True
                                if i < len(self.matrix) - 1:
                                    for obj in self.matrix[i+1][j]:
                                        for dop_rule in self.level_rules:
                                            if f'{obj.name} is stop' in dop_rule.text_rule\
                                                    or f'{obj.name} is push' in dop_rule.text_rule\
                                                    or f'{obj.name} is pull' in dop_rule.text_rule\
                                                    or rule_object.name == obj.name\
                                                    or obj.text:
                                                status_clone = False
                                    if status_clone:
                                        copy_matrix[i+1][j].append(Object(j,
                                                                          i+1,
                                                                          rule_object.direction,
                                                                          rule_object.name,
                                                                          rule_object.text)
                                                                   )
                                    status_clone = True
                                    if j < len(self.matrix[i]) - 1:
                                        for obj in self.matrix[i][j + 1]:
                                            for dop_rule in self.level_rules:
                                                if f'{obj.name} is stop' in dop_rule.text_rule \
                                                        or f'{obj.name} is push' in dop_rule.text_rule \
                                                        or f'{obj.name} is pull' in dop_rule.text_rule\
                                                        or rule_object.name == obj.name\
                                                        or obj.text:
                                                    status_clone = False
                                        if status_clone:
                                            copy_matrix[i][j + 1].append(Object(j + 1,
                                                                                i,
                                                                                rule_object.direction,
                                                                                rule_object.name,
                                                                                rule_object.text)
                                                                         )
                                    status_clone = True
                                    if j > 0:
                                        for obj in self.matrix[i][j - 1]:
                                            for dop_rule in self.level_rules:
                                                if f'{obj.name} is stop' in dop_rule.text_rule \
                                                        or f'{obj.name} is push' in dop_rule.text_rule \
                                                        or f'{obj.name} is pull' in dop_rule.text_rule \
                                                        or rule_object.name == obj.name\
                                                        or obj.text:
                                                    status_clone = False
                                        if status_clone:
                                            copy_matrix[i][j - 1].append(Object(j - 1,
                                                                                i,
                                                                                rule_object.direction,
                                                                                rule_object.name,
                                                                                rule_object.text)
                                                                         )
                                    status_clone = True
                                    if i > 0:
                                        for obj in self.matrix[i - 1][j]:
                                            for dop_rule in self.level_rules:
                                                if f'{obj.name} is stop' in dop_rule.text_rule \
                                                        or f'{obj.name} is push' in dop_rule.text_rule \
                                                        or f'{obj.name} is pull' in dop_rule.text_rule \
                                                        or rule_object.name == obj.name\
                                                        or obj.text:
                                                    status_clone = False
                                        if status_clone:
                                            copy_matrix[i - 1][j].append(Object(j,
                                                                                i - 1,
                                                                                rule_object.direction,
                                                                                rule_object.name,
                                                                                rule_object.text)
                                                                         )
                            if f'{rule_object.name} is move' in rule.text_rule:
                                if rule_object.direction == 0:
                                    if not rule_object.move_up(copy_matrix, self.level_rules):
                                        rule_object.direction = 2
                                if rule_object.direction == 1:
                                    if not rule_object.move_right(copy_matrix, self.level_rules):
                                        rule_object.direction = 3
                                if rule_object.direction == 2:
                                    if not rule_object.move_down(copy_matrix, self.level_rules):
                                        rule_object.direction = 0
                                if rule_object.direction == 3:
                                    if not rule_object.move_left(copy_matrix, self.level_rules):
                                        rule_object.direction = 1

                            if f'{rule_object.name} is nudge' in rule.text_rule:
                                if f'{rule_object.name} is nudgedown' in rule.text_rule:
                                    rule_object.move_down(
                                        copy_matrix, self.level_rules, 'push')
                                if f'{rule_object.name} is nudgedup' in rule.text_rule:
                                    rule_object.move_up(
                                        copy_matrix, self.level_rules, 'push')
                                if f'{rule_object.name} is nudgeleft' in rule.text_rule:
                                    rule_object.move_left(
                                        copy_matrix, self.level_rules, 'push')
                                if f'{rule_object.name} is nudgeright' in rule.text_rule:
                                    rule_object.move_right(
                                        copy_matrix, self.level_rules, 'push')

                        rule_object.is_hot = is_hot
                        rule_object.is_hide = is_hide
                        rule_object.locked_sides = my_deepcopy(locked_sides)

        if self.matrix != copy_matrix:
            self.history_of_matrix.append(self.matrix)
            self.matrix = my_deepcopy(copy_matrix)

        if self.status_cancel:
            if len(self.history_of_matrix) > 0:
                self.matrix = self.copy_matrix(self.history_of_matrix[-1])
                self.history_of_matrix = my_deepcopy(
                    self.history_of_matrix[:-1])
            else:
                self.matrix = self.copy_matrix(self.start_matrix)

        if not flag:
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

        self.level_rules = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.check_horizontally(i, j)
                self.check_vertically(i, j)
        self.level_rules = self.remove_copies_rules(self.level_rules)

        if not flag:
            for line in self.matrix:
                for cell in line:
                    for game_object in cell:
                        game_object.draw(self.screen)

        self.animation_level()

        if state is None:
            state = State(GameState.flip, None)
        return state
