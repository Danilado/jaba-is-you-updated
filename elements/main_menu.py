from typing import List, Optional

import pygame

import settings
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.editor import Editor
from elements.game import Game
from elements.level_loader import Loader
from elements.global_classes import GuiSettings, sound_manager
from global_types import SURFACE


class MainMenu(GameStrategy):
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self._state: Optional[State] = None
        pygame.mixer.init()
        sound_manager.get_music("sounds/menu")

    def _start_the_game(self):
        self._state = State(GameState.switch, Game)

    def _go_to_editor(self):
        self._state = State(GameState.switch, Editor)

    def _exit_the_game(self):
        self._state = State(GameState.stop, None)

    def _go_to_loader(self):
        self._state = State(GameState.switch, Loader)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        buttons = [
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 - 120, 400, 50, (0, 0, 0),
                   GuiSettings(), "Начать играть", self._start_the_game),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 - 60, 400, 50, (0, 0, 0),
                   GuiSettings(), "Мультиплеер"),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2, 400, 50, (0, 0, 0),
                   GuiSettings(), "Редактор уровней", self._go_to_editor),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 + 60, 400, 50, (0, 0, 0),
                   GuiSettings(), "Уровни", self._go_to_loader),
            Button(settings.RESOLUTION[0] // 2 - 200, settings.RESOLUTION[1] // 2 + 120, 400, 50, (0, 0, 0),
                   GuiSettings(), "Выйти", self._exit_the_game),
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
                self._state = State(GameState.flip, None)
        return self._state
