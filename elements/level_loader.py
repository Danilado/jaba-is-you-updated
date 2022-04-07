import glob
import re
from functools import partial
from typing import List, Optional

import pygame

import settings
from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State
from elements.play_level import PlayLevel
from elements.global_classes import GuiSettings, palette_manager
from global_types import SURFACE
from utils import language_words


class Loader(GameStrategy):
    """
    Класс загрузчика уровней. На данный момент используется для
    поиска файлов уровней в папке и их первичной обработки
    """

    def music(self):
        pass

    def __init__(self, screen: SURFACE, from_editor_overlay=None, plug=None):
        """Инициализация загрузчика

        :param screen: На какую поверхность отрисовываться
        :type screen: SURFACE
        :param from_editor_overlay: Показывает пришёл игрок из редактора или меню, defaults to None
        :type from_editor_overlay: EditorOverlay, optional
        :param plug:
            Параметр - затычка. Используется во избежание крашей
            игры при входе из редактора (unused), defaults to None
        :type plug: Any, optional
        """
        super().__init__(screen)
        self.overlay = from_editor_overlay
        self._state: Optional[State] = None
        self.lang_words = language_words()
        self.buttons = [
            Button(settings.RESOLUTION[0] // 2 - int(600 * settings.WINDOW_SCALE),
                   settings.RESOLUTION[1] // 2 - int(400 * settings.WINDOW_SCALE),
                   int(1200 * settings.WINDOW_SCALE), int(50 * settings.WINDOW_SCALE), (0, 0, 0), GuiSettings(),
                   f"{self.lang_words[10]}",
                   self.go_back),
        ]
        for index, level in enumerate(self.find_levels()):
            self.buttons.append(
                Button(settings.RESOLUTION[0] // 2 - int(600 * settings.WINDOW_SCALE),
                       settings.RESOLUTION[1] // 2 - int(350 * settings.WINDOW_SCALE)
                       + int(50 * index * settings.WINDOW_SCALE),
                       int(1200 * settings.WINDOW_SCALE), int(50 * settings.WINDOW_SCALE), (0, 0, 0), GuiSettings(),
                       level,
                       partial(self.go_to_game if self.overlay is None else self.return_and_quit, level)),
            )

    def go_to_game(self, level_name: str):
        """
        Осуществляет переход в игровую стратегию отрисовки матрицы.

        :param level_name: Название желаемого уровня
        :type level_name: str
        """
        # Gospodin: Надеюсь, когда-нибудь это будет игрой.
        self._state = State(GameState.SWITCH, partial(PlayLevel, level_name))

    def go_back(self):
        """Простая отмена (выход в предыдущее меню)"""
        self._state = State(GameState.BACK)

    def return_and_quit(self, level_name: str):
        """
        Метод, использующийся для взаимодействия с редактором.
        Парсит необходимый уровень из файла в матрицу и
        передаёт её в редактор через его оверлей управления

        :param level_name: Название желаемого уровня
        """
        self.overlay.loaded_flag = True
        self.overlay.editor.current_state = self.parse_file(level_name)
        self.overlay.editor.level_name = level_name
        self._state = State(GameState.BACK)

    def parse_file(self, level_name: str) -> List[List[List[Object]]]:
        """
        Преобразует записанную в файле уровня информацию в матрицу

        :param level_name: Название желаемого уровня
        :return: Возвращает преобразованную из файла матрицу
        """
        matrix: List[List[List[Object]]] = [[[]
                                             for _ in range(32)] for _ in range(18)]
        leve_file = open(f'./levels/{level_name}.omegapog_map_file_type_MLG_1337_228_100500_69_420',
                         'r', 'utf-8')
        lines = leve_file.read().split('\n')
        for line_index, line in enumerate(lines):
            # TODO by quswadress: Very similar to the method parse_file of Draw class.
            parameters = line.strip().split(' ')
            if len(parameters) > 1:
                matrix[int(parameters[1])][int(parameters[0])].append(Object(
                    int(parameters[0]),
                    int(parameters[1]),
                    int(parameters[2]),
                    parameters[3],
                    False if parameters[4] == 'False' else True,
                ))
            elif line_index == 0:
                self.overlay.editor.current_palette = palette_manager.get_palette(
                    parameters[0])
        return matrix

    @staticmethod
    def find_levels() -> List[str]:
        """
        Поиск уровней в папке levels

        :return: Список с путями к уровням в виде строк
        """
        levels_arr: List[str] = []
        for entry in glob.glob("levels/*.omegapog_map_file_type_MLG_1337_228_100500_69_420"):
            levels_arr.append(re.split(r'[/\\]', entry.split('.')[0])[1])
        return levels_arr

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
                    self._state = State(GameState.BACK)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._state = State(GameState.BACK)
            for button in self.buttons:
                button.draw(self.screen)
                button.update(events)
            if self._state is None:
                self._state = State(GameState.FLIP, None)
        return self._state
