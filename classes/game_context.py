from pprint import pprint
from typing import Final, TYPE_CHECKING, Callable, List, Optional, Union, Type

import pygame

from classes.game_state import GameState

if TYPE_CHECKING:
    from classes.game_strategy import GameStrategy
from settings import RESOLUTION, FRAMES_PER_SECOND, DEBUG


class GameContext:
    def __init__(self, game_strategy: Union[Callable[[pygame.surface.Surface], "GameStrategy"], Type["GameStrategy"]]):
        self.screen: Final[pygame.surface.Surface] = pygame.display.set_mode(RESOLUTION)
        self._running: bool = True
        self._history: List[GameStrategy] = []
        self._game_strategy: Optional[GameStrategy] = None
        self.game_strategy = game_strategy  # type: ignore
        # См. https://github.com/python/mypy/issues/3004

    @property
    def game_strategy(self) -> Optional["GameStrategy"]:
        return self._game_strategy

    @game_strategy.setter
    def game_strategy(self, game_strategy: Union[Callable[[pygame.surface.Surface], "GameStrategy"], "GameStrategy"]):
        if callable(game_strategy):
            self._game_strategy = game_strategy(self.screen)
        else:
            self._game_strategy = game_strategy
        if len(self._history) > 1 and self._history[-2] == self._game_strategy:
            del self._history[-1]
        else:
            self._history.append(self._game_strategy)
        if DEBUG:
            print(f'Current game strategy is {self._game_strategy.__class__.__name__}; History a.k.a stack: ', end="")
            pprint([game_strategy.__class__.__name__ for game_strategy in self._history], indent=4)

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value

    @property
    def history(self) -> List["GameStrategy"]:
        return self._history

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            try:
                delta_time = clock.tick(FRAMES_PER_SECOND)
                pygame.display.set_caption(f"{clock.get_fps()} FPS; {self.game_strategy.__class__.__name__}")
                events = pygame.event.get()
                draw_state = self.game_strategy.draw(events, delta_time)
                if draw_state is not None:
                    if draw_state.game_state is GameState.stop:
                        raise KeyboardInterrupt
                    elif draw_state.game_state is GameState.switch:
                        self.game_strategy = draw_state.switch_to
                    elif draw_state.game_state is GameState.flip:
                        pygame.display.flip()
                    elif draw_state.game_state is GameState.back:
                        if len(self.history) > 1:
                            self.game_strategy = self.history[-2]
                        else:
                            raise ValueError("Can't back; Use debug to show the history of strategies; ")
                    else:
                        raise ValueError(f"draw_state.game_state: {draw_state.game_state}. WTF is this!?")
            except KeyboardInterrupt:
                self.running = False
