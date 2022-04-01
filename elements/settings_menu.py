from typing import List, Optional

import pygame

from classes.slider import Slider
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.state import State
from elements.global_classes import GuiSettings
from global_types import SURFACE
from settings import RESOLUTION
from utils import settings_saves


class SettingsMenu(GameStrategy):
    def music(self):
        pass

    def __init__(self, screen: SURFACE):
        super().__init__(screen)
        self.flag_to_move_circle = False
        self._state: Optional[State] = None
        self.options = settings_saves()

        x = int(RESOLUTION[0] // 2 + 200 + 400 * pygame.mixer.music.get_volume())
        y = int(RESOLUTION[1] // 2 - 300 + 3)
        self.circle_music = [x, y]

        self.slider = Slider(RESOLUTION[0] // 2 + 200, RESOLUTION[1] // 2 - 300, 400, 6, (50, 10, 250),
                             self.circle_music, 5, (250, 100, 250), self.set_music_volume)
        self.buttons = [
            Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 180, 1200, 50, (0, 0, 0),
                   GuiSettings(), "Выключить сетку", self.set_show_grid),
            Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 120, 1200, 50, (0, 0, 0),
                   GuiSettings(), "Язык: Русский", self.set_language),
            Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 60, 1200, 50, (0, 0, 0),
                   GuiSettings(), "Назад", self.go_back),
        ]

    def save_file(self):
        with open('option_settings', mode='w', encoding='utf-8') as file:
            for index, param in enumerate(self.options):
                file.write(f'{param}\n')
            file.close()

    def go_back(self):
        """Простая отмена (выход в предыдущее меню)"""
        self.save_file()
        self._state = State(GameState.BACK)

    def set_language(self):
        if self.options[1] == 'Ru':
            self.options[1] = 'Eng'
        else:
            self.options[1] = 'Ru'

    def set_show_grid(self):
        if self.options[0]:
            self.options[0] = False
        else:
            self.options[0] = True

    def set_music_volume(self):
        if pygame.mouse.get_pos()[0] > RESOLUTION[0] // 2 + 200:
            if RESOLUTION[0] // 2 + 200 + 400 > pygame.mouse.get_pos()[0]:
                self.circle_music[0] = int(pygame.mouse.get_pos()[0])
            else:
                self.circle_music[0] = RESOLUTION[0] // 2 + 200 + 400
        else:
            self.circle_music[0] = RESOLUTION[0] // 2 + 200
        pygame.mixer.music.set_volume((self.circle_music[0] - (RESOLUTION[0] // 2 + 200)) / 400)
        self.options[2] = pygame.mixer.music.get_volume()

    def check_options(self):
        if self.options[0]:
            if self.options[1] == 'Ru':
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 180, 1200, 50, (0, 0, 0),
                                         GuiSettings(), "Выключить сетку", self.set_show_grid)
            else:
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 180, 1200, 50, (0, 0, 0),
                                         GuiSettings(), "Turn off grid", self.set_show_grid)
        else:
            if self.options[1] == 'Ru':
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 180, 1200, 50, (0, 0, 0),
                                         GuiSettings(), "Включить сетку", self.set_show_grid)
            else:
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 180, 1200, 50, (0, 0, 0),
                                         GuiSettings(), "Turn on grid", self.set_show_grid)

        if self.options[1] == 'Ru':
            self.buttons[1] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 120, 1200, 50, (0, 0, 0),
                                     GuiSettings(), "Язык: Русский", self.set_language)
            self.buttons[2] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 60, 1200, 50, (0, 0, 0),
                                     GuiSettings(), "Назад", self.go_back)
        else:
            self.buttons[1] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 120, 1200, 50, (0, 0, 0),
                                     GuiSettings(), "Language: English", self.set_language)
            self.buttons[2] = Button(RESOLUTION[0] // 2 - 600, RESOLUTION[1] // 2 - 60, 1200, 50, (0, 0, 0),
                                     GuiSettings(), "Back", self.go_back)

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
            f2 = pygame.font.SysFont('fonts/ConsolateElf.ttf', 24)
            if self.options[1] == 'Ru':
                text1 = f2.render('Громкость музыки', False, (255, 255, 255))
            else:
                text1 = f2.render('Music volume', False, (255, 255, 255))
            self.screen.blit(text1, (RESOLUTION[0] // 2 + 200 - 175, RESOLUTION[1] // 2 - 300 - 6))
            for event in events:
                if event.type == pygame.QUIT:
                    self._state = State(GameState.BACK)
                    self.save_file()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_file()
                        self._state = State(GameState.BACK)
            self.check_options()
            self.slider.update(events)
            self.slider.draw(self.screen)
            for button in self.buttons:
                button.draw(self.screen)
                button.update(events)
            if self._state is None:
                self._state = State(GameState.FLIP, None)
        return self._state
