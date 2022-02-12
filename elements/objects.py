import pygame

pygame.font.init()
font = pygame.font.SysFont('segoeuisemibold', 15)


# Абстрактный, но нет
class Object:
    """
        Создание:
        obj = Object(аргументы)

        Аргументы - Строго по порядку:

        x -         Позиция объекта на сетке уровня по оси х
        y -         Позиция объекта на сетке уровня по оси y
        direction - Направление, в которое смотрит объект во
                    время создания
                    Может принимать следующие значения:
                    0 - Вверх
                    1 - Вправо
                    2 - Вниз
                    3 - Влево
                    Используется с правилами move, turn,
                    shift и т.д.
        name -      Название объекта
                    Важно! По названию определяется и
                    текстурка объекта на поле!
        rules -     Правила игры на момент появления объекта
        is_text -   Булевая переменная определяющая является
                    объект текстом, или нет
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

    def __init__(self, x=None, y=None, direction=None, name: str = "empty", rules=None, is_text: bool = True):
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
        # self.images                                                                       # unimplemented
        # Всё далее должно заполняться с помощью поступающих правил
        self.solid = 0
        self.z_index = 1
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

    def draw(self, screen):
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

    def unparse(self):
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'
