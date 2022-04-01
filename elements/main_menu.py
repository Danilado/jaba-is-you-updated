from typing import List, Optional

import pygame

import settings
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.settings_menu import SettingsMenu
from elements.editor import Editor
from elements.level_loader import Loader
from elements.global_classes import GuiSettings, sound_manager
from elements.map_menu import MapMenu
from global_types import SURFACE
from utils import language_words


class MainMenu(GameStrategy):
    """
    Стратегия главного меню
    """

    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self._state: Optional[State] = None
        sound_manager.load_music("sounds/Music/menu")

    def _start_the_game(self):
        self._state = State(GameState.SWITCH, MapMenu)

    def _go_to_editor(self):
        self._state = State(GameState.SWITCH, Editor)

    def _exit_the_game(self):
        self._state = State(GameState.STOP, None)

    def _go_to_loader(self):
        self._state = State(GameState.SWITCH, Loader)

    def _go_to_options(self):
        self._state = State(GameState.SWITCH, SettingsMenu)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int):
        buttons = [
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 - 120, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[0]}", self._start_the_game),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 - 60, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[1]}"),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[2]}", self._go_to_editor),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 + 60, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[3]}", self._go_to_loader),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 + 120, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[4]}", self._go_to_options),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 + 180, 400, 50, (0, 0, 0),
                   GuiSettings(), f"{language_words()[5]}", self._exit_the_game),
        ]
        self._state = None
        if events:
            self.screen.fill("black")
            for event in events:
                if event.type == pygame.QUIT:
                    self._exit_the_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._exit_the_game()
            for button in buttons:
                button.draw(self.screen)
                button.update(events)
            if self._state is None:
                self._state = State(GameState.FLIP, None)
        return self._state

    def music(self):
        sound_manager.load_music("sounds/Music/menu")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
