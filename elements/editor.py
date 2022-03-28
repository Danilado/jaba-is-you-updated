from datetime import datetime
from functools import partial
from math import ceil
from typing import List, Optional

import pygame

from classes.button import Button
from classes.game_state import GameState
from classes.game_strategy import GameStrategy
from classes.object_button import ObjectButton
from classes.objects import Object
from classes.palette import Palette
from classes.state import State
from elements.global_classes import EuiSettings, IuiSettings, sound_manager, palette_manager
from elements.overlay import EditorOverlay
from settings import SHOW_GRID, RESOLUTION, OBJECTS, STICKY
from utils import my_deepcopy


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


def direction_to_unicode(direction: int) -> str:
    """
    Направление в юникод-стрелку

    :param direction:
        0 - Вверх
        1 - Вправо
        2 - Вниз
        3 - Влево
    :return: Один символ - Юникод-стрелка
    """
    return '↑' if direction == 1 else '→' if direction == 0 else '↓' if direction == 3 else '←'


class Editor(GameStrategy):
    """Класс редактора уровней

    :param GameStrategy: Является игровой стратегией и наследуется
    от соответственного класса
    """

    def __init__(self, screen: pygame.Surface):
        """Класс редактора уровней

        :param screen: Окно для отрисовки
        :type screen: pygame.Surface
        """
        super().__init__(screen)
        # overlay related
        self.exit_flag = False
        self.discard = False
        self.level_name = None
        self.state = None
        self.first_iteration = True
        self.new_loaded = False
        # tools
        self.tool = 1
        self.direction = 1
        self.is_text = False
        self.name: Optional[str] = None
        # history
        self.changes: List[List[List[List[Object]]]] = []
        # matrix state
        self.current_state: List[List[List[Object]]] = [
            [[] for _ in range(32)] for _ in range(18)]
        # focused cell
        self.focus = (-1, -1)
        # buttons
        self.buttons: List[ObjectButton] = []
        self.page = 0
        self.pagination_limit = ceil(len(OBJECTS) / 12)
        self.pagination_buttons = [
            Button(RESOLUTION[0] + 17, RESOLUTION[1] - 222, 75, 20, (0, 0, 0), IuiSettings(),
                   "<", partial(self.page_turn, -1)),
            Button(RESOLUTION[0] + 101, RESOLUTION[1] - 222, 75, 20, (0, 0, 0), IuiSettings(),
                   ">", partial(self.page_turn, 1)),
        ]
        # quswadress' palette logic
        self._current_palette: Palette = palette_manager.get_palette("default")
        # features
        self.screen = pygame.display.set_mode((1800, 900))
        self.page_turn(0)
        self.empty_object = Object(-1, -1, 0, 'empty', is_text=False, palette=self.current_palette)

    def save(self, state, name=None):
        """Сохранение трёхмерного массива в память

        :param state: Трёхмерный массив состояния сетки
        :type state: list
        """
        string = f"{self.current_palette.name}\n"
        string_state, counter = unparse_all(state)
        string += string_state
        print(name)
        if name is None:
            name = 'autosave_' + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        with open(f"levels/{name}.omegapog_map_file_type_MLG_1337_228_100500_69_420", 'w',
                  encoding='utf-8') as file:
            file.write(string)

    def page_turn(self, number: int):
        """Меняет страницу списка объектов

        :param n: Вперёд или назад перелистывать и на какое количество страниц
        :type n: int
        """
        self.page = (self.page + number) % self.pagination_limit
        self.buttons = self.parse_buttons()

    def parse_buttons(self):
        """
        Даёт список из 12-и или менее кнопок, расположенных на странице кнопок (?),
        в которой в данный момент находится редактор

        :return: массив кнопок
        :rtype: list
        """
        button_objects_array = OBJECTS[12 * self.page:12 * (self.page + 1)]
        button_array = []
        for index, text in enumerate(button_objects_array):
            button_array.append(
                ObjectButton(x=RESOLUTION[0] + 28 + 84 * (index % 2),
                             y=25 + 55 * (index - index % 2), width=50, height=50, outline=(0, 0, 0),
                             settings=EuiSettings(), text=text, action=partial(self.set_name, text),
                             is_text=self.is_text, direction=self.direction, movement_state=0,
                             palette=self.current_palette))
        return button_array

    def unresize(self):
        """Меняет разрешение экрана с расширенного на изначальное через магические константы 1600х900"""
        self.screen = pygame.display.set_mode((1600, 900))

    def safe_exit(self):
        """Функция подготовки к безопасному выходу из редактора без потери изменений"""
        print(self.level_name)
        self.save(self.current_state, self.level_name)
        self.unresize()

    def extreme_exit(self):
        """Функция подготовки к безопасному выходу из редактора без потери изменений"""
        self.save(self.current_state, None)
        self.unresize()

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
        self.direction = (self.direction - direction) % 4
        self.page_turn(0)

    def set_tool(self, number: int):
        """Функция смены инструмента

        :param n: [0 - 2], где 0 - удалить, 1 - создать, а 2 - исследовать клетку и вывести содержимое в консоль
        :type n: int
        """
        self.tool = number

    def is_text_swap(self):
        """Меняет является ли объект текстом, или нет"""
        self.is_text = not self.is_text
        self.page_turn(0)

    def undo(self):
        """Отменяет последнее изменение"""
        if len(self.changes) != 0:
            self.current_state = self.changes[-1]
            self.changes.pop()
            for line in self.current_state:
                for cell in line:
                    for game_object in cell:
                        if game_object.name in STICKY and not game_object.is_text:
                            neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.neighbours = neighbours
                            game_object.animation = game_object.animation_init()

    def get_neighbours(self, y, x) -> List[Object]:
        """Ищет соседей клетки сверху, справа, снизу и слева

        :param y: координата на матрице по оси y идёт первым,
        потому что ориентирование на матрице происходит зеркально относительно нормального
        :type y: int
        :param x: координата на матрице по оси x
        :type x: int
        :return: Массив с четырьмя клетками-соседями в порядке сверху, справа, снизу, слева
        :rtype: List[]
        """
        offsets = [
            (0, -1),
            (1,  0),
            (0,  1),
            (-1, 0),
        ]
        neighbours = [None for _ in range(4)]
        if x == 0:
            neighbours[0] = [self.empty_object]
        elif x == RESOLUTION[1]//50-1:
            neighbours[2] = [self.empty_object]

        if y == 0:
            neighbours[3] = [self.empty_object]
        elif y == RESOLUTION[0]//50-1:
            neighbours[1] = [self.empty_object]

        for index, offset in enumerate(offsets):
            if neighbours[index] is None:
                neighbours[index] = self.current_state[x +
                                                       offset[1]][y + offset[0]]
        return neighbours

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
                neighbours = []
                if self.name in STICKY and not self.is_text:
                    # ЭТО НУЖНО ДЕЛАТЬ ДО ДОБАВЛЕНИЯ В МАТРИЦУ
                    neighbours = self.get_neighbours(
                        self.focus[0], self.focus[1])
                self.changes.append(my_deepcopy(self.current_state))
                self.current_state[self.focus[1]][self.focus[0]].append(
                    Object(x=self.focus[0], y=self.focus[1], direction=self.direction, name=self.name,
                           is_text=self.is_text, movement_state=0, neighbours=neighbours, palette=self.current_palette))
                if self.name in STICKY and not self.is_text:
                    # ЭТО НУЖНО ДЕЛАТЬ ПОСЛЕ ДОБАВЛЕНИЯ ОБЪЕКТА В МАТРИЦУ
                    for array in neighbours:
                        for neighbour in array:
                            if neighbour.name in STICKY and not neighbour.is_text:
                                neighbour.neighbours = self.get_neighbours(
                                    neighbour.x, neighbour.y)
                                neighbour.animation = neighbour.animation_init()

    def delete(self):
        """Если в клетке есть объекты, удаляет последний созданный из них"""
        # ? Нужно ли выбирать что удалять?
        if len(self.current_state[self.focus[1]][self.focus[0]]) > 0:
            self.changes.append(my_deepcopy(self.current_state))
            self.current_state[self.focus[1]][self.focus[0]].pop()
            neighbours = self.get_neighbours(
                self.focus[0], self.focus[1])
            for array in neighbours:
                for neighbour in array:
                    if neighbour.name in STICKY and not neighbour.is_text:
                        neighbour.neighbours = self.get_neighbours(
                            neighbour.x, neighbour.y)
                        neighbour.animation = neighbour.animation_init()

    def overlay(self):
        """Вызывает меню управления редактора"""
        self.unresize()
        self.state = State(GameState.SWITCH, partial(EditorOverlay, self))

    @property
    def current_palette(self) -> Palette:
        return self._current_palette

    @current_palette.setter
    def current_palette(self, value: Palette):
        self._current_palette = value
        self.buttons = self.parse_buttons()
        for state in self.changes + [self.current_state]:
            for line in state:
                for cell in line:
                    for rule_object in cell:
                        rule_object.palette = value
                        rule_object.animation = rule_object.animation_init()
                        print(rule_object.name, "aaaaaaaa", value.name)

    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        """Отрисовывает редактор (включая все его элементы) и обрабатывает все действия пользователя

        :param events: События, собранные окном pygame
        :type events: List[pygame.event.Event]
        :param delta_time_in_milliseconds:
            Время между нынешним
            и предыдущим кадром (unused)
        :type delta_time_in_milliseconds: int
        :return: Возвращает состояние для правильной работы game_context
        :rtype: Optional[State]
        """

        self.state = None
        if self.first_iteration:
            self.first_iteration = False
            self.overlay()
        if self.exit_flag:
            if not self.discard:
                self.safe_exit()
            self.state = State(GameState.BACK)
            self.unresize()
        if self.new_loaded:
            self.changes.clear()
            self.new_loaded = False
            for line in self.current_state:
                for cell in line:
                    for game_object in cell:
                        if game_object.name in STICKY and not game_object.is_text:
                            neighbours = self.get_neighbours(
                                game_object.x, game_object.y)
                            game_object.neighbours = neighbours
                            game_object.animation = game_object.animation_init()

        self.screen.fill("black")
        for event in events:
            if event.type == pygame.QUIT:
                self.extreme_exit()
                self.state = State(GameState.BACK)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.overlay()
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
                   f"Text\n{'True' if self.is_text else 'False'}", self.is_text_swap),
            Button(RESOLUTION[0] + 17, RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Tool\n{'Create' if self.tool == 1 else 'Delete' if self.tool == 0 else 'Lookup'}",
                   partial(self.set_tool, 0 if self.tool == 1 else 1 if self.tool == 2 else 2)),
            Button(RESOLUTION[0] + 101, RESOLUTION[1] - 100, 75, 75, (0, 0, 0), IuiSettings(),
                   f"Dir\n{direction_to_unicode(self.direction)}",
                   partial(self.turn, 1)),
        ]

        pygame.draw.rect(self.screen, (44, 44, 44),
                         (self.focus[0] * 50, self.focus[1] * 50, 50, 50))

        if SHOW_GRID:
            for i in range(RESOLUTION[0] // 50 + 1):  # Отрисовать сетку
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (i * 50, 0), (i * 50, RESOLUTION[1]), 1)
            for i in range(RESOLUTION[1] // 50 + 1):
                pygame.draw.line(self.screen, (255, 255, 255), (0, i * 50 - (1 if i == 18 else 0)),
                                 (RESOLUTION[0], i * 50 - (1 if i == 18 else 0)), 1)

        for button in self.buttons:
            if self.state is None and button.update(events) and button.action is exit:
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

        if self.state is None:
            self.state = State(GameState.FLIP)
        return self.state

    def music(self):
        sound_manager.load_music("sounds/Music/editor")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
