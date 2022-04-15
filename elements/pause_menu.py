import pygame

import settings
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.global_classes import GuiSettings, sound_manager
from elements.main_menu import MainMenu
from elements.map_menu import MapMenu
from global_types import SURFACE
from typing import List, Optional

from utils import language_words


class PauseMenu(GameStrategy):
    """
    Стратегия меню паузы
    """

    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self.screen.set_alpha(None)
        self._state: Optional[State] = None

    def _return_to_game(self):
        self._state = State(GameState.BACK)

    def _go_to_level_menu(self):
        self._state = State(GameState.SWITCH, MapMenu)

    def _go_to_main_menu(self):
        self._state = State(GameState.SWITCH, MainMenu)

    def _exit_the_game(self):
        self._state = State(GameState.STOP, None)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int):
        buttons = [
            Button(settings.RESOLUTION[0] // 2 - int(200 * settings.WINDOW_SCALE),
                   settings.RESOLUTION[1] // 2 - int(180 * settings.WINDOW_SCALE),
                   int(400 * settings.WINDOW_SCALE), int(50 * settings.WINDOW_SCALE),
                   (0, 0, 0), GuiSettings(), f"{language_words()[20]}",
                   self._return_to_game),
            Button(settings.RESOLUTION[0] // 2 - int(200 * settings.WINDOW_SCALE),
                   settings.RESOLUTION[1] // 2 - int(120 * settings.WINDOW_SCALE),
                   int(400 * settings.WINDOW_SCALE), int(50 * settings.WINDOW_SCALE),
                   (0, 0, 0), GuiSettings(), f"{language_words()[21]}",
                   self._go_to_level_menu),
            Button(settings.RESOLUTION[0] // 2 - int(200 * settings.WINDOW_SCALE),
                   settings.RESOLUTION[1] // 2 - int(60 * settings.WINDOW_SCALE),
                   int(400 * settings.WINDOW_SCALE), int(50 * settings.WINDOW_SCALE),
                   (0, 0, 0), GuiSettings(), f"{language_words()[22]}",
                   self._go_to_main_menu),
        ]
        self._state = None

        self.screen.fill("black")

        for event in events:
            if event.type == pygame.QUIT:
                self._exit_the_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._return_to_game()
        for button in buttons:
            button.draw(self.screen)
            button.update(events)
        if self._state is None:
            self._state = State(GameState.FLIP, None)
        else:
            pygame.event.set_allowed(None)

        return self._state

    def on_init(self):
        sound_manager.load_music("sounds/Music/menu")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        pygame.event.set_allowed(
            [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONUP])
        print("QUIT, KEYDOWN, MOUSEBUTTONUP")
