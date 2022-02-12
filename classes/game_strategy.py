import abc
from typing import List, Optional

import pygame

from classes.state import State


class GameStrategy(abc.ABC):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    @abc.abstractmethod
    def draw(self, events: List[pygame.event.Event], delta_time_in_milliseconds: int) -> Optional[State]:
        ...
