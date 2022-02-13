import abc
from typing import List, Optional

import pygame

from classes.state import State


class GameStrategy(abc.ABC):
    """
    Абстрактный класс, необходимый для определения отрисовки меню в GameContext.

    :ivar screen: Экран на котором будет происходить вся отрисовка.
    """
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen

    @abc.abstractmethod
    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        """

        :param events: Cписок событий
        :param delta_time_in_milliseconds: время прошедшее между кадрами для не зависимого от FPS, движения
        :return: Изменение в игре, см. :class:`classes.game_state.GameState`

        .. note::
            Если этот метод вернёт None, то ничего, в том числе и обновление экрана, не произойдёт.
            Для обновления экрана, верните State(GameState.flip)
        """
        ...
