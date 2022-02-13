import pygame

pygame.font.init()
font = pygame.font.SysFont('segoeuisemibold', 15)


# Абстрактный, но нет
class Object:

    def __init__(self, x=None, y=None, direction=None, name: str = "empty", rules=None, is_text: bool = True):
        """Класс всех объектов на экране

        :param x: Позиция объекта на экране по оси X ПО СЕТКЕ, defaults to None
        :type x: int, optional
        :param y: Позиция объекта на экране по оси Y ПО СЕКТЕ, defaults to None
        :type y: int, optional
        :param direction: Направление объекта, где 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево, defaults to None
        :type direction: int, optional
        :param name: Название объекта. Работает с правилами и текстурой для отрисовки, defaults to "empty"
        :type name: str, optional
        :param rules: Правила игры во время создания объекта, defaults to None
        :type rules: list, optional
        :param is_text: Определяет является ли объект текстом, defaults to True
        :type is_text: bool, optional
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
        # self.images # unimplemented
        # Всё далее должно заполняться с помощью поступающих правил
        self.solid = 0 # Будет ли происходить коллизия с игроком. Св-ва stop, push
        self.z_index = 1 # Высота, или приоритет отрисовки. Зависит от самого объекта, или св-ва float
        # Следующие строки для более-менее оптимизированной отрисовки букв. Нужно заменить спрайтами и т.д. 
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

    def draw(self, screen):
        """Отрисовывает объект класса Object на экране

        :param screen: Окно, в котором будет происходить отрисовка
        :type screen: pygame.Surface
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

    def unparse(self):
        """Переводит объект класса Object в достаточную для сохранения в файле форму

        :return: Строка для сохранения
        :rtype: str
        """
        return f'{self.x} {self.y} {self.direction} {self.name} {self.text}'
