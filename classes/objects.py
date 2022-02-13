from typing import Union, Optional

import pygame

pygame.font.init()
font = pygame.font.SysFont('segoeuisemibold', 15)


# TODO: Too many fields, refactor this please!
# Абстрактный, но нет
class Object:
    """
    Объект правил, например, jaba, you, is, and, и т.д

    :ivar x: Позиция объекта на **сетке** уровня по оси х
    :ivar y: Позиция объекта на **сетке** уровня по оси y
    :ivar xpx: Абсцисса объекта на **экране** по оси х
    :ivar ypx: Ордината объекта на **экране** по оси y

    :ivar direction:
        Направление, в которое смотрит объект во время создания. Может принимать следующие значения:
        0 - Вверх
        1 - Вправо
        2 - Вниз
        3 - Влево
        Используется с правилами move, turn,
        shift и т.д.

    :ivar name: Название объекта
    :ivar is_text: Переменная определяющая является объект текстом, или нет

    :ivar width: Ширина спрайта
    :ivar height: Высота спрайта
    """
    def debug(self):
        return print(f"""
-- {self.x} {self.y} ---
x:          {self.x}
y:          {self.y}
direction:  {self.direction}
name:       {self.name}
is_text:    {self.text}
--- {(len(str(self.x)) + len(str(self.y))) * ' '} ---
        """)   # TODO: Use logger library

    def __init__(self, x: int, y: int, direction: int = 0, name: str = "empty", is_text: bool = True):
        """
        Инициализация объекта

        :param x: Позиция объекта на **сетке** уровня по оси х
        :param y: Позиция объекта на **сетке** уровня по оси y

        :param direction:
            Направление, в которое смотрит объект во время создания. Может принимать следующие значения:
            0 - Вверх
            1 - Вправо
            2 - Вниз
            3 - Влево
            Используется с правилами move, turn,
            shift и т.д.

        :param name: Название объекта

        .. important:: По названию определяется и текстурка объекта на поле!

        :param is_text: Переменная определяющая является объект текстом, или нет
        """
        self.name = name
        self.text = is_text
        self.direction = direction  # Используется с правилами move, turn, shift и т.д.
        self.x = x  # Не по пикселям, а по сетке!
        self.y = y  # Не по пикселям, а по сетке!
        self.xpx = x * 50 if self.x is not None else None  # По пикселям
        self.ypx = y * 50 if self.y is not None else None  # По пикселям
        self.width = 50
        self.height = 50
        self.renderable_text = self.name[0:1] + '\n' + self.name[2:3]  # Временный костыль пока нет текстур
        # quswadress: Все остальные переменные являются временными костылями, и не добавлены в доку
        # self.images                                                                       # unimplemented
        # Всё далее должно заполняться с помощью поступающих правил
        # self.solid = 0
        # self.z_index = 1
        # Что-то ещё?
        lines = self.renderable_text.split('\n')
        self.width_lines = []
        self.height_lines = []
        self.text_height = 0
        self.lines = []
        for line in lines:
            self.lines.append(font.render(line, True, (255, 255, 255)))
            self.width_lines.append(self.lines[-1].get_width())
            self.height_lines.append(self.lines[-1].get_height())
            self.text_height += self.height_lines[-1]

    def draw(self, screen: Union[pygame.Surface, pygame.surface.Surface]):
        """
        Метод отрисовки кнопки

        :param screen: Surface, на котором будет происходить отрисовка
        """
        if self.text:
            for i in range(len(self.lines)):
                screen.blit(
                    self.lines[i],
                    (
                        self.xpx + (self.width / 2 - self.width_lines[i] / 2),
                        self.ypx + (self.height / 2 + (self.text_height / len(self.lines) *
                                                       (len(self.lines) // 2 * -1 + i))) -
                        (self.height_lines[i] / 2 if len(self.lines) == 1 else 0)
                    )
                )

    def unparse(self) -> str:
        """Сериализовать объект в строку"""
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'
