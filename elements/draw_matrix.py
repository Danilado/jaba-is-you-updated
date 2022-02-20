from typing import List, Optional

import pygame

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION


class Draw(GameStrategy):
    """
    Стратегия отрисовки уровня.

    :ivar matrix: Список списков списка объектов. То есть, карта объектов в игре.
    :ivar screen: Экран на котором будет происходить вся отрисовка.
    """
    def __init__(self, level_name: str, screen: SURFACE):
        super().__init__(screen)
        self.matrix: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.parse_file(level_name)

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
                parameters = line.split(' ')
                if len(parameters) > 1:
                    self.matrix[int(parameters[1])][int(parameters[0])].append(Object(
                        int(parameters[0]),
                        int(parameters[1]),
                        int(parameters[2]),
                        parameters[3],
                        False if parameters[4] == 'False' else True
                    ))

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
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 50, 50), 1)
        
        for line in self.matrix:
            for cell in line:
                for object in cell:
                    object.draw(self.screen)

        if state is None:
            state = State(GameState.flip, None)
        return state
