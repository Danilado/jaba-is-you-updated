import os
from functools import partial
from math import ceil
from typing import List, Optional

import pygame

from classes.button import Button
from classes.object_button import ObjectButton
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.objects import Object
from classes.state import State
from elements.global_classes import EuiSettings, IuiSettings, sound_manager
from settings import SHOW_GRID, RESOLUTION, OBJECTS


def my_deepcopy(arr):
    """Полное копирование трёхмерного массива без использования указателей

    :param arr: Исходный массив
    :type arr: list
    :return: Копия в других ячейках памяти
    :rtype: list
    """
    new_arr = []
    for val in arr:
        if isinstance(val, list):
            new_arr.append(my_deepcopy(val))
        else:
            new_arr.append(val)
    return new_arr


def unparse_all(state):
    """Создание строки для сохранения состояния сетки в файл за одну запись если он не пустой

    :param state: Трёхмерный массив состояния сетки
    :type state: list
    :return: Строка для записи
    :rtype: str
    """
    string = ''
    counter = 0
    for row in state:
        for cell in row:
            for game_object in cell:
                counter += 1
                string += game_object.unparse() + '\n'
    return string, counter


def save(state):
    """Сохранение трёхмерного массива в память

    :param state: Трёхмерный массив состояния сетки
    :type state: list
    """
    string, counter = unparse_all(state)
    if counter > 0:
        with open(f"levels/level{len(os.listdir('levels/'))}.omegapog_map_file_type_MLG_1337_228_100500_69_420", 'w',
                  encoding='utf-8') as file:
            file.write(string)


class Editor(GameStrategy):
    def __init__(self, screen: pygame.Surface):
        """Класс редактора уровней

        :param screen: Окно для отрисовки
        :type screen: pygame.Surface
        """
        super().__init__(screen)
        self.tool = 1
        self.direction = 1
        self.is_text = False
        self.name: Optional[str] = None
        self.changes: List[List[List[List[Object]]]] = []
        self.current_state: List[List[List[Object]]] = [[[] for _ in range(32)] for _ in range(18)]
        self.focus = (-1, -1)
        self.buttons: List[ObjectButton] = []
        self.page = 0
        self.pagination_limit = ceil(len(OBJECTS) / 12)
        self.pagination_buttons = [
            Button(RESOLUTION[0] + 17, RESOLUTION[1] - 222, 75, 20, (0, 0, 0), IuiSettings(),
                   f"<", partial(self.page_turn, -1)),
            Button(RESOLUTION[0] + 101, RESOLUTION[1] - 222, 75, 20, (0, 0, 0), IuiSettings(),
                   f">", partial(self.page_turn, 1)),
        ]
        self.screen = pygame.display.set_mode((1800, 900))
        self.page_turn(0)

    def page_turn(self, n: int):
        """Меняет страницу списка объектов

        :param n: Вперёд или назад перелистывать и на какое количество страниц
        :type n: int
        """
        self.page = (self.page + n) % self.pagination_limit
        self.buttons = self.parse_buttons()

    def parse_buttons(self):
        """
        Даёт список из 10-и или менее кнопок, расположенных на странице кнопок (?),
        в которой в данный момент находится редактор

        :return: массив кнопок
        :rtype: list
        """
        button_objects_array = OBJECTS[12 * self.page:12 * (self.page + 1)]
        button_array = []
        for index, text in enumerate(button_objects_array):
            # print(f'{index+1} {text}')
            button_array.append(
                ObjectButton(RESOLUTION[0] + 28 + 84 * (index % 2), 25 + 55 * (index - index % 2), 50, 50, (0, 0, 0),
                             EuiSettings(), text, partial(self.set_name, text), self.is_text, self.direction))
        return button_array

    def safe_exit(self):
        """Функция подготовки к безопасному выходу из редактора без потери изменений"""
        self.screen = pygame.display.set_mode((1600, 900))
        save(self.current_state)

    def set_name(self, string: str):
        """Функция смены названия объекта, а следовательно текстур и правил.

        :param string: Новое название объекта
        :type string: str
        """
        self.name = string

    def turn(self, direction: int):
        """Функция поворота объекта

        :param direction: направление, где 1 - по часовой стрелке, а -1 - против часовой
        """
        self.direction = (self.direction + direction) % 4
        self.page_turn(0)

    def set_tool(self, n: int):
        """Функция смены инструмента

        :param n: [0 - 2], где 0 - удалить, 1 - создать, а 2 - исследовать клетку и вывести содержимое в консоль 
        :type n: int
        """
        self.tool = n

    def is_text_swap(self):
        """Меняет является ли объект текстом, или нет
        """
        self.is_text = False if self.is_text else True 
        self.page_turn(0)

    def undo(self):
        """Отменяет последнее изменение
        """
        if len(self.changes) != 0:
            self.current_state = self.changes[-1]
            self.changes.pop()

    def create(self):
        """
        Если в выделенной клетке нет объекта с таким же именем, создаёт его там и
        записывает предыдущее состояние сетки в архивный массив
        """
        if self.name is not None:
            flag = 0
            for game_object in self.current_state[self.focus[1]][self.focus[0]]:
                if game_object.name == self.name:
                    flag = 1
                    break
            if not flag:
                self.changes.append(my_deepcopy(self.current_state))
                self.current_state[self.focus[1]][self.focus[0]].append(
                    Object(self.focus[0], self.focus[1], self.direction, self.name, self.is_text))

    def delete(self):
        """Если в клетке есть объекты, удаляет последний созданный из них
        """
        # ? Нужно ли выбирать что удалять?
        if len(self.current_state[self.focus[1]][self.focus[0]]) > 0:
            self.changes.append(my_deepcopy(self.current_state))
            self.current_state[self.focus[1]][self.focus[0]].pop()

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        # TODO: Refactor this. There is "Long Method"
        state = None
        self.screen.fill("black")
        for event in events:
            if event.type == pygame.QUIT:
                self.safe_exit()
                state = State(GameState.back)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.safe_exit()
                    state = State(GameState.back)
                if event.key == pygame.K_e:
                    self.turn(1)
                if event.key == pygame.K_q:
                    self.turn(-1)
                if event.key == pygame.K_t:
                    self.is_text_swap()
                if event.key == pygame.K_x:
                    self.set_tool(0)
                if event.key == pygame.K_c:
                    self.set_tool(1)
                if event.key == pygame.K_a:
                    self.set_tool(2)
                if event.key == pygame.K_TAB:
                    self.page_turn(1)
                if event.key == pygame.K_z and event.mod == 4160:
                    self.undo()
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] <= 1600:
                    self.focus = (event.pos[0] // 50, event.pos[1] // 50)
                else:
                    self.focus = (-1, -1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.focus[0] != -1:
                    if self.tool == 1:
                        self.create()
                    elif self.tool == 0:
                        self.delete()
                    else:
                        print(self.current_state[self.focus[1]][self.focus[0]])

        indicators = [
            Button(RESOLUTION[0] + 17, RESOLUTION[1] - 192, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Obj\n{self.name}"),
            Button(RESOLUTION[0] + 101, RESOLUTION[1] - 192, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Text\n{'True' if self.is_text == 1 else 'False'}", self.is_text_swap),
            Button(RESOLUTION[0] + 17, RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Tool\n{'Create' if self.tool == 1 else 'Delete' if self.tool == 0 else 'Lookup'}",
                   partial(self.set_tool, 0 if self.tool == 1 else 1 if self.tool == 2 else 2)),
            Button(RESOLUTION[0] + 101, RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Dir\n{'↑' if self.direction == 0 else '→' if self.direction == 1 else '↓' if self.direction == 2 else '←'}",
                   partial(self.turn, 1)),
        ]

        pygame.draw.rect(self.screen, (44, 44, 44), (self.focus[0] * 50, self.focus[1] * 50, 50, 50))

        if SHOW_GRID:
            for i in range(RESOLUTION[0] // 50 + 1):  # Отрисовать сетку
                pygame.draw.line(self.screen, (255, 255, 255), (i * 50, 0), (i * 50, RESOLUTION[1]), 1)
            for i in range(RESOLUTION[1] // 50 + 1):
                pygame.draw.line(self.screen, (255, 255, 255), (0, i * 50 - (1 if i == 18 else 0)),
                                 (RESOLUTION[0], i * 50 - (1 if i == 18 else 0)), 1)

        for button in self.buttons:
            if state is None and button.update(events) and button.action is exit:
                break
            button.draw(self.screen)
        for pagination_button in self.pagination_buttons:
            pagination_button.update(events)
            pagination_button.draw(self.screen)
        for indicator in indicators:
            indicator.update(events)
            indicator.draw(self.screen)

        for line in self.current_state:
            for cell in line:
                for object_button in cell:
                    object_button.draw(self.screen)

        if state is None:
            state = State(GameState.flip)
        return state

    def music(self):
        sound_manager.get_music("sounds/Music/editor")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

    def replay_music(self):
        pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
