import os
from functools import partial
from math import ceil
from typing import List, Optional

import pygame

from classes.button import Button
from classes.input import Input
from classes.object_button import ObjectButton
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State
from elements import editor
from elements.global_classes import GuiSettings, EuiSettings
from elements.level_loader import Loader
from settings import RESOLUTION


class EditorOverlay(GameStrategy):
    """Оверлей управления редактором уровней

    :param GameStrategy: Наследуется от базового класса игровой 
    стратегии
    """

    def __init__(self, screen: pygame.Surface, editor, plug=None):
        """Инициализирует оверлей

        :param screen: На какой поверхности отрисовывать
        :type screen: pygame.Surface
        :param editor: Экземпляр класса Editor, который и управляет 
        оверлей
        :type editor: Editor
        :param plug: Параметр - затычка. Используется во избежание 
        крашей игры (unused), defaults to None
        :type plug: _type_, optional
        """
        super().__init__(screen)
        self.state = None
        self.editor = editor
        self.loaded_flag = False
        self.label = self.editor.level_name
        print(self.editor.level_name, self.label)
        if self.label is None:
            self.label = "Новый уровень"
        print(self.editor.level_name, self.label)
        self.buttons = [
            Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 180, 400, 50, (0, 0, 0),
                   EuiSettings(), f"Вы изменяете {self.label}"),
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
        ]

    def save(self):
        """Сохраняет матрицу редактора
        """
        self.editor.safe_exit()

    def cancel(self):
        """Отменяет вход в оверлей и возвращает к редактору
        """
        self.state = State(GameState.back)

    def load(self):
        """Делает автосейв изменений в редакторе, если они есть, и 
        вызывает загрузчик для загрузки уровня в редактор"""
        self.editor.extreme_exit()
        self.state = State(GameState.switch, partial(
            Loader, self.screen, self))

    def force_exit(self):
        """Осуществляет выход из редактора с сохранением"""
        self.state = State(GameState.back)
        self.editor.exit_flag = True

    def hard_force_exit(self):
        """Осуществляет выход без сохранения"""
        self.state = State(GameState.back)
        self.editor.exit_flag = True
        self.editor.discard = True

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        """Отрисовывает оверлей управления редактором и обрабатывает события

        :param events: События, собранные окном pygame
        :type events: List[pygame.event.Event]
        :param delta_time_in_milliseconds: Время между нынешним 
        и предыдущим кадром (unused)
        :type delta_time_in_milliseconds: int
        :return: Возвращает состояние для правильной работы game_context
        """
        self.state = State(GameState.back) if self.loaded_flag else None
        self.screen.fill('black')

        for event in events:
            if event.type == pygame.QUIT:
                self.state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.editor.levelname = str(self.buttons[3])
                    self.state = State(GameState.back)
            if event.type == pygame.KEYUP:
                if str(self.buttons[3]) != '' and str(self.buttons[3]) != None:
                    self.label = str(self.buttons[3])
                self.buttons[0] = Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2 - 180, 400, 50, (0, 0, 0),
                                         EuiSettings(), f"Вы изменяете {self.label}")

        for button in self.buttons:
            if self.state is None and button.update(events) and button.action is exit:
                break
            button.draw(self.screen)

        if self.state != None:
            if str(self.buttons[3]) != '' and str(self.buttons[3]) != None:
                self.editor.level_name = str(self.buttons[3])
                if self.editor.level_name == '':
                    self.editor.level_name = None
            self.screen = pygame.display.set_mode((1800, 900))
        if self.state is None:
            self.state = State(GameState.flip)
        return self.state
