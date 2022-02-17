from typing import List, Optional

import pygame

from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.player import Player
from classes.state import State
from global_types import SURFACE
from settings import SHOW_GRID, RESOLUTION


class Game(GameStrategy):
    """
    Класс игры

    :ivar jaba: Игрок
    """
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self.jaba = Player(0, 0)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        state = None
        self.screen.fill("black")

        for event in events:
            if event.type == pygame.QUIT:
                state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = State(GameState.back)
        self.jaba.check_events(events)
        self.jaba.move()
        self.jaba.cancel_move()

        self.jaba.draw(self.screen)
        if SHOW_GRID:
            for x in range(0, RESOLUTION[0], 50):
                for y in range(0, RESOLUTION[1], 50):
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 50, 50), 1)
        if state is None:
            state = State(GameState.flip)
        return state
