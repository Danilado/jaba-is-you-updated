from multiprocessing.spawn import import_main_path
from typing import Union, TYPE_CHECKING, Callable, Any, Optional, List, Sequence
from elements.global_classes import sprite_manager
from classes.animation import Animation
from settings import TEXT_ONLY

import os, os.path
import pygame

if TYPE_CHECKING:
    from elements.global_classes import COLOR, AbstractButtonSettings


class Button:
    """
    Класс кнопки

    :ivar x: Абсцисса положения
    :ivar y: Ордината положения
    :ivar width: Ширина в пикселях
    :ivar height: Высота в пикселях
    :ivar outline: Цвет контура
    :ivar settings: Настройка цветов
    :ivar text: Текст
    :ivar action: Функция вызывающаяся при нажатии
    """
    def __init__(self, x: int, y: int, width: int, height: int, outline: "COLOR", settings: "AbstractButtonSettings",
                 text: Union[str, bytes] = "", action: Optional[Callable[[], Any]] = None):
        """
        Инициализация кнопки

        :param x: Абсцисса положения
        :param y: Ордината положения
        :param width: Ширина в пикселях
        :param height: Высота в пикселях
        :param outline: Цвет контура
        :param settings: Настройка цветов
        :param text: Текст
        :param action: Функция вызывающаяся при нажатии
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.settings = settings
        self.action = action
        self.outline = outline

    def draw(self, screen: Union[pygame.Surface, pygame.surface.Surface]):
        """
        Метод отрисовки кнопки

        :param screen: Surface, на котором будет происходить отрисовка
        """
        if self.outline:
            pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        color = self.settings.button_color if not self.is_over(
            pygame.mouse.get_pos()) else self.settings.button_color_hover
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            pygame.font.init()
            font = pygame.font.SysFont('segoeuisemibold', self.settings.text_size)
            lines = self.text.split('\n')
            text_height = 0
            for index, line in enumerate(lines):
                line = font.render(line, True, (255, 255, 255))
                text_height += line.get_height()
                screen.blit(
                    line,
                    (
                        self.x + (self.width / 2 - line.get_width() / 2),
                        self.y + (self.height / 2 + (text_height / len(lines) *
                                                     (len(lines) // 2 * -1 + index))) -
                        (line.get_height() / 2 if len(lines) == 1 else 0)
                    )
                )

    def update(self, events: List[pygame.event.Event]) -> bool:
        """
        Метод проверки нажатия.

        :param events: Список событий полученных путём вызова pygame.event.get()
        :return: В случае если был вызван action, True, иначе False
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN \
                    and self.is_over(pygame.mouse.get_pos()) \
                    and self.action:
                self.action()
                return True
        return False

    def is_over(self, pos: Sequence[Union[int, float]]) -> bool:
        """
        Проверка координат на нахождение внутри области кнопки

        :param pos: Абсцисса и Ордината для проверки наведения

        :return: True, если Абсцисса и Ордината находится в области кнопки, иначе False.
        """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class ObjectButton(Button):
    def __init__(self, x, y, width, height, outline, settings, text="", action=None, is_text = 0, direction = 1):
        super().__init__(x, y, width, height, outline, settings, text, action)
        if is_text or self.text in TEXT_ONLY:
            self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/words/{self.text}/{self.text}{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
        else:
            DIR = f'./sprites/{self.text}'
            sprite_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            state_count = sprite_count // 3
            letterize = {
                0: 'b',
                1: 'r',
                2: 'f',
                3: 'l',
            }
            if state_count > 4:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.text}/{self.text}{letterize[direction]}0{index}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            elif state_count > 1:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.text}/{self.text}{letterize[direction]}{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))
            else:
                self.animation = Animation(
                    [pygame.transform.scale(sprite_manager.get(f"sprites/{self.text}/{self.text}{index+1}"),
                    (50, 50)) for index in range(0, 3)], 200, (self.x, self.y))


    def draw(self, screen: pygame.Surface):
        self.animation.update()
        self.animation.draw(screen)
