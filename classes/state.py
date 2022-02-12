from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Type
    from classes.game_state import GameState
    from classes.game_strategy import GameStrategy


@dataclass
class State:
    game_state: "GameState"
    switch_to: "Optional[Type[GameStrategy]]" = None
