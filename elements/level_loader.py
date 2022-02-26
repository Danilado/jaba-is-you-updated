import glob
from functools import partial
from typing import List, Optional

import pygame

from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.draw_matrix import Draw
from elements.global_classes import GuiSettings
from global_types import SURFACE
from settings import RESOLUTION


class Loader(GameStrategy):
    """
    Стратегия загрузки уровня.

    :ivar buttons: Список кнопок
    """
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self._state: Optional[State] = None
        self.buttons = [
            Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 400, 1200, 50, (0, 0, 0),
                   GuiSettings(), "Назад", self.go_back),
        ]
        for index, level in enumerate(self.find_levels()):
            self.buttons.append(
                Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 350 + 50 * index, 1200, 50, (0, 0, 0),
                       GuiSettings(), level, partial(self.go_to_game, level)),
            )

    def go_to_game(self, level_name: str):
        """
        Смена стратегии на :attr:`~elements.draw_matrix.Draw`.

        :param level_name: Название уровня в папке levels
        """
        self._state = State(GameState.switch, partial(Draw, level_name))

    def go_back(self):
        """Вернуться на прошлую стратегию"""
        self._state = State(GameState.back)

    @staticmethod
    def find_levels() -> List[str]:
        """
        Поиск уровней в папке levels

        :return: Список с путями к уровням в виде строк
        """
        levels_arr: List[str] = []
        for entry in glob.glob("levels/*.omegapog_map_file_type_MLG_1337_228_100500_69_420"):
            levels_arr.append(entry.split('.')[0].split('\\')[1])
        return levels_arr

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
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
            for button in self.buttons:
                button.draw(self.screen)
                button.update(events)
            if self._state is None:
                self._state = State(GameState.flip, None)
        return self._state
