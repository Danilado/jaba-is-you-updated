from typing import Final, Tuple, Sequence

DEBUG: bool = True

RESOLUTION: Final[Tuple[int, int]] = (1600, 900)  # 32x18
SHOW_GRID: Final[bool] = True
FRAMES_PER_SECOND: Final[int] = 60  # Свободно дополняйте.

TEXT_ONLY: Final[Sequence[str]] = (
    'is', 'and', 'stop', 'push', 'defeat', 'win', 'you', 'move', 'not', 'me', 'ok', 'cash', 'back', 'best',
    'safe', 'sad', 'has', 'all', 'bonus', 'cloud', 'sink', 'swap', 'tele', 'text', 'tree', 'ufo', 'stick',
    'statue', 'spike', 'sleep', 'shut', 'shirt', 'shift', 'safe', 'rubble', 'rocket', 'right', 'red', 'blue',
    'pull', 'powered', 'power', 'play', 'pillar', 'p2', 'P1', 'orb', 'open', 'on', 'near', 'move',
    'more', 'melt', 'make', 'love', 'lonely', 'line', 'level', 'left', 'idle', 'husk', 'hot', 'hide', 'hedge',
    'has', 'group', 'fungus', 'fungi', 'fruit', 'follow', 'foliage', 'flower',
    'float', 'fall', 'facing', 'end', 'empty', 'eat', 'dust', 'down', 'dot', 'done', 'defeat', 'cursor', 'cog',
    'cloud', 'cliff', 'chill', 'bubble', 'brick', 'box', 'bonus', 'bolt', 'bog', 'anni', 'algae'
)

OBJECTS: Final[Sequence[str]] = (*TEXT_ONLY, 'cake', 'fire', 'ghost',
                                 'rock', 'door', 'skull', 'tile', 'bird', 'bat', 'bird', 'bug',
                                 'rose', 'bat', 'flag', 'hand', 'key', 'sun', 'stump', 'star', 'moon',
                                 'leaf', 'ladder', 'fear', 'door', 'cup'
                                 )
