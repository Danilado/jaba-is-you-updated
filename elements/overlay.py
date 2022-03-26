from functools import partial
from typing import List, Optional, TYPE_CHECKING

import pygame

from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.input import Input
from classes.state import State
from elements.global_classes import GuiSettings, EuiSettings
from elements.level_loader import Loader
from elements.palette_choose import PaletteChoose
from settings import RESOLUTION

if TYPE_CHECKING:
    from elements.editor import Editor


class EditorOverlay(GameStrategy):
    """
    Оверлей управления редактором уровней
    """

    def music(self):
        pass

    def __init__(self, editor: "Editor", screen: pygame.Surface):
        """Инициализирует оверлей

        :param screen: На какой поверхности отрисовывать
        :param editor: Экземпляр класса Editor, который и управляет оверлей
        """
        super().__init__(screen)
        self.state = None
        self.editor: "Editor" = editor
        self.loaded_flag = False
        self.label = self.editor.level_name
        if self.label is None:
            self.label = "Новый уровень"
        self.buttons = [
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 280, 400, 50, (0, 0, 0),
                   EuiSettings(), f"Вы изменяете {self.label}"),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 230, 400, 50, (0, 0, 0),
                   EuiSettings(), f"Текущая палитра: {self.editor.current_palette.name}"),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 120, 400, 50, (0, 0, 0),
                   GuiSettings(), "Назад", self.cancel),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 60, 400, 50, (0, 0, 0),
                   GuiSettings(), "Загрузить уровень", self.load),
            Input(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2, 400, 50, (255, 255, 255),
                  EuiSettings(), "Новое название"),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 + 60, 400, 50, (0, 0, 0),
                   GuiSettings(), "Сохранить", self.save),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 + 120, 400, 50, (0, 0, 0),
                   GuiSettings(), "Сохранить и выйти в главное меню", self.force_exit),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 + 180, 400, 50, (0, 0, 0),
                   GuiSettings(), "Выйти без сохранения", self.hard_force_exit),
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 180, 400, 50, (0, 0, 0),
                   GuiSettings(), f"Поменять палитру", self.switch_to_palette_choose),
        ]

    def save(self):
        """Сохраняет матрицу редактора
        """
        self.editor.safe_exit()

    def cancel(self):
        """Отменяет вход в оверлей и возвращает к редактору
        """
        self.state = State(GameState.BACK)

    def load(self):
        """
        Делает автоматическое сохранение изменений в редакторе, если они есть,
        и вызывает загрузчик для загрузки уровня в редактор
        """
        self.editor.extreme_exit()
        self.state = State(GameState.SWITCH, partial(
            Loader, self.screen, self))

    def force_exit(self):
        """Осуществляет выход из редактора с сохранением"""
        self.state = State(GameState.BACK)
        self.editor.exit_flag = True

    def hard_force_exit(self):
        """Осуществляет выход без сохранения"""
        self.state = State(GameState.BACK)
        self.editor.exit_flag = True
        self.editor.discard = True

    def switch_to_palette_choose(self):
        self.state = State(GameState.SWITCH, partial(
            PaletteChoose, self.editor))

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        """Отрисовывает оверлей управления редактором и обрабатывает события

        :param events: События, собранные окном pygame
        :type events: List[pygame.event.Event]
        :param delta_time_in_milliseconds: Время между нынешним и предыдущим кадром (unused)
        :type delta_time_in_milliseconds: int
        :return: Возвращает состояние для правильной работы game_context
        """
        self.state = State(GameState.BACK) if self.loaded_flag else None
        self.editor.new_loaded = bool(self.loaded_flag)
        self.screen.fill('black')

        for event in events:
            if event.type == pygame.QUIT:
                self.state = State(GameState.BACK)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.editor.level_name = str(self.buttons[4])
                    self.state = State(GameState.BACK)
            if event.type == pygame.KEYUP:
                if str(self.buttons[4]):
                    self.label = str(self.buttons[4])
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 280, 400, 50, (0, 0, 0),
                                         EuiSettings(), f"Вы изменяете {self.label}")
                self.buttons[1].text = f"Текущая палитра: {self.editor.current_palette.name}"

        for button in self.buttons:
            button.update(events)
            button.draw(self.screen)

        if self.state is not None:
            if str(self.buttons[3]) != '':
                self.editor.level_name = str(self.buttons[4])
                if self.editor.level_name == '':
                    self.editor.level_name = None
            self.screen = pygame.display.set_mode((1800, 900))
        if self.state is None:
            self.state = State(GameState.FLIP)
        return self.state
