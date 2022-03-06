from typing import List, Optional
from functools import partial

import pygame

from elements.global_classes import sound_manager
from elements.draw_matrix import Draw

from settings import SHOW_GRID, RESOLUTION, LEVELS_PASSED
from global_types import SURFACE

from classes.cursor import MoveCursor
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State


class Map_menu(GameStrategy):
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self.matrix: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.matrix = self.parse_file(self.find_map_menu())
        self.cursor = MoveCursor()

    def go_to_game(self):
        for i in range(len(self.matrix)):
            for j in range((len(self.matrix[i]))):
                for k in range(len(self.matrix[i][j])):
                    if k < len(self.matrix[i][j]) and j < 31:
                        if self.matrix[i][j][k].name == 'cursor' and self.matrix[i][j][k].text == False:
                            self._state = State(GameState.switch, partial(Draw, self.matrix[i][j][0].name.split("/")[1]))

    @staticmethod
    def parse_file(level_name: str) -> List[List[List[Object]]]:
        matrix: List[List[List[Object]]] = [[[]
                                             for _ in range(32)] for _ in range(18)]
        leve_file = open(
            f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420', 'r')
        lines = leve_file.read().split('\n')
        for line in lines:
            parameters = line.split(' ')
            if len(parameters) > 1:
                matrix[int(parameters[1])][int(parameters[0])].append(Object(
                    int(parameters[0]),
                    int(parameters[1]),
                    int(parameters[2]),
                    parameters[3],
                    False if parameters[4] == 'False' else True
                ))
        return matrix

    def find_cursor_pos(self):
        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    if game_object == 'cursor':
                        return game_object.x, game_object.y
        return 0,0

    def find_map_menu(self):
        if LEVELS_PASSED < 7:
            map = 'map1'
        elif 15 > LEVELS_PASSED >= 7:
            map = 'map2'
        else:
            map = 'map'
        return map


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
        if events:
            self.screen.fill("black")
            for event in events:
                if event.type == pygame.QUIT:
                    self._state = State(GameState.back)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._state = State(GameState.back)
                    if event.key == pygame.K_RETURN:
                        self.go_to_game()

        self.cursor.check_events(events)
        self.cursor.move(self.matrix)

        if SHOW_GRID:
            for x in range(0, RESOLUTION[0], 50):
                for y in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(
                        self.screen, (255, 255, 255), (x, y, 50, 50), 1)

        for line in self.matrix:
            for cell in line:
                for game_object in cell:
                    game_object.draw(self.screen)


        if self._state is None:
            self._state = State(GameState.flip, None)

        return self._state

    def music(self):
        sound_manager.load_music("sounds/Music/burn")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
