from typing import List, Optional
from functools import partial

import pygame

from elements.global_classes import sound_manager
from elements.play_level import PlayLevel

from settings import SHOW_GRID, RESOLUTION, STICKY
from global_types import SURFACE

from classes.cursor import MoveCursor
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State


class MapMenu(GameStrategy):
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self.levels_passed = 0
        self.matrix: List[List[List[Object]]] = [[[]
                                                  for _ in range(32)] for _ in range(18)]
        self.cursor = MoveCursor()
        self._state: Optional[State] = None
        self.first_iteration = True
        self.moved = False
        self.parse_file(self.find_map_menu())
        self.empty_object = Object(-1, -1, 0, 'empty', False)
        self.radius = 0
        self.flag_anime = False
        self.delay = 0

    def animation_level(self):
        if self.flag_anime:
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 0), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (600, 0), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1000, 0), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1600, 0), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 900), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (300, 900), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (800, 900), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1200, 900), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 300), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30), (0, 600), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1600, 100), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1600, 500), self.radius)
            pygame.draw.circle(self.screen, (0, 50, 30),
                               (1600, 900), self.radius)
            self.radius += 8

    def parse_file(self, level_name: str):
        """
        Парсинг уровней. Добавляет объекты в :attr:`~.Draw.matrix`.

        .. note::
            Если вы хотите перезаписать карту, не забудьте удалить объекты из :attr:`~.Draw.matrix`

        :param level_name: Название уровня в папке levels
        :raises OSError: Если какая либо проблема с открытием файла.
        """
        with open(f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420',
                  'r', encoding='utf-8') as level_file:
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
            (1, 0),
            (0, 1),
            (-1, 0),
        ]
        neighbours = [None for _ in range(4)]
        if x == 0:
            neighbours[0] = [self.empty_object]
        elif x == RESOLUTION[1] // 50 - 1:
            neighbours[2] = [self.empty_object]

        if y == 0:
            neighbours[3] = [self.empty_object]
        elif y == RESOLUTION[0] // 50 - 1:
            neighbours[1] = [self.empty_object]

        for index, offset in enumerate(offsets):
            if neighbours[index] is None:
                neighbours[index] = self.matrix[x + offset[1]][y + offset[0]]
        return neighbours

    def go_to_game(self):
        for i, line in enumerate(self.matrix):
            for j, cell in enumerate(line):
                for k, rule_object in enumerate(cell):
                    if k < len(cell) and j < 31:
                        if rule_object.name == 'cursor' and not rule_object.is_text:
                            if self.matrix[i][j][0].name in self.cursor.levels:
                                self._state = State(GameState.SWITCH, partial(PlayLevel,
                                                                              self.matrix[i][j][0].name.split("/")[0]))
                            if self.matrix[i][j][0].name in self.cursor.reference_point:
                                pass

    def find_map_menu(self):
        if self.levels_passed < 7:
            level_map = 'map'
        elif 15 > self.levels_passed >= 7:
            level_map = 'map'
        else:
            level_map = 'map'
        return level_map

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        """Отрисовывает интерфейс загрузчика и обрабатывает все события

        :param events: События, собранные окном pygame
        :type events: List[pygame.event.Event]
        :param delta_time_in_milliseconds: Время между нынешним и предыдущим кадром (unused)
        :type delta_time_in_milliseconds: int
        :return: Возвращает состояние для правильной работы game_context
        """
        self.screen.fill("black")
        self._state = None

        self.screen.fill("black")
        for event in events:
            if event.type == pygame.QUIT:
                self._state = State(GameState.BACK)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._state = State(GameState.BACK)
                if event.key == pygame.K_RETURN:
                    self.delay = pygame.time.get_ticks()
                    self.flag_anime = True

        if not self.flag_anime:
            self.cursor.check_events(events)
            self.cursor.move(self.matrix)

        if SHOW_GRID:
            for xpx in range(0, RESOLUTION[0], 50):
                for ypx in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255), (xpx, ypx, 50, 50), 1)

        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    if self.first_iteration or self.moved:
                        if game_object.name in STICKY and not game_object.is_text:
                            neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.neighbours = neighbours
                            game_object.animation = game_object.animation_init()
                    game_object.draw(self.screen)

        if self.first_iteration:
            self.first_iteration = False

        if self.moved:
            self.moved = False

        if self.flag_anime:
            self.animation_level()
            if pygame.time.get_ticks() - self.delay > 1500:
                self.flag_anime = False
                self.radius = 0
                self.go_to_game()

        if self._state is None:
            self._state = State(GameState.FLIP, None)

        return self._state

    def music(self):
        sound_manager.load_music("sounds/Music/burn")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
