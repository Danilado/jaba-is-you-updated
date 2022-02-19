from typing import List, Optional
from functools import partial

import pygame
import glob, os

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION
from classes.objects import Object
from elements.global_classes import GuiSettings


class Draw(GameStrategy):
    def __init__(self, levelname: str, screen: SURFACE):
        super().__init__(screen)
        self.matrix: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.parse_file(levelname)

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

        if self._state is None:
            self._state = State(GameState.flip, None)
        return self._state
