from typing import List, Optional

import pygame

import settings
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.editor import Editor
from elements.game import Game
from elements.global_classes import GuiSettings
from global_types import SURFACE


class MainMenu(GameStrategy):
    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self._state: Optional[State] = None

    def _start_the_game(self):
        self._state = State(GameState.switch, Game)

    def _go_to_editor(self):
        self._state = State(GameState.switch, Editor)

    def _exit_the_game(self):
        self._state = State(GameState.stop, None)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int):
        buttons = [
            Button(414, 462, 770, 65, (0, 0, 0),
                   GuiSettings(), "Продолжить играть на 1 слоте", self._start_the_game),
            Button(262, 552, 492, 65, (0, 0, 0),
                   GuiSettings(), "Чит-панель"),
            Button(262, 619, 492, 65, (0, 0, 0),
                   GuiSettings(), "Редактор уровней", self._go_to_editor),
            Button(262, 686, 492, 65, (0, 0, 0),
                   GuiSettings(), "Создатели"),
            Button(847, 552, 492, 65, (0, 0, 0),
                   GuiSettings(), "Другие уровни"),
            Button(847, 619, 492, 65, (0, 0, 0),
                   GuiSettings(), "Настройки"),
            Button(847, 686, 492, 65, (0, 0, 0),
                   GuiSettings(), "Выйти из игры", self._exit_the_game),
        ]
        self._state = None
        if events:
            try:
                background_file = "images/background.jpeg"
                img = pygame.image.load(background_file)
                img = pygame.transform.scale(img, settings.RESOLUTION)
                img = img.convert_alpha()
                self.screen.blit(img, (0, 0))
            except:
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
