from typing import Final, Tuple, Sequence

DEBUG: bool = True

RESOLUTION: Final[Tuple[int, int]] = (1600, 900)  # 32x18
SHOW_GRID: Final[bool] = True
FRAMES_PER_SECOND: Final[int] = 60  # Свободно дополняйте.

TEXT_ONLY: Final[Sequence[str]] = (
    'is', 'and', 'stop', 'push', 'defeat', 'win', 'you', 'move', 'not', 'me', 'ok', 'back', 'best',
    'safe', 'sad', 'has', 'all', 'bonus', 'cloud', 'sink', 'swap', 'tele', 'text', 'stick',
    'statue', 'spike', 'sleep', 'shut', 'shift', 'safe', 'right', 'red', 'blue', 'pillar',
    'pull', 'powered', 'play', 'p2', 'P1', 'orb', 'open', 'on', 'near', 'move', 'rubble',
    'more', 'melt', 'make', 'lonely', 'line', 'level', 'left', 'idle', 'husk', 'hot', 'hide', 'hedge',
    'has', 'group', 'follow', 'foliage', 'float', 'fall', 'facing', 'end', 'empty', 'eat', 'down',
    'dot', 'done', 'defeat', 'cloud', 'cliff', 'chill', 'brick', 'bonus', 'bolt', 'bog', 'anni', 'algae',
)

PIPES: Final[Sequence[str]] = (
    'pipe/pipe_solo', 'pipe/pipe_b', 'pipe/pipe_bf', 'pipe/pipe_br', 'pipe/pipe_brf', 'pipe/pipe_f', 'pipe/pipe_l',
    'pipe/pipe_lb', 'pipe/pipe_lbf', 'pipe/pipe_lbrf', 'pipe/pipe_lbr',
    'pipe/pipe_lf', 'pipe/pipe_lrf', 'pipe/pipe_r', 'pipe/pipe_rf',
)

LETTERS: Final[Sequence[str]] = ('words/a', 'words/b', 'words/c', 'words/d', 'words/e', 'words/f', 'words/g', 'words/h', 'words/i', 'words/l'
                                 )


OBJECTS: Final[Sequence[str]] = (*TEXT_ONLY, *PIPES, *LETTERS, 'cake', 'fire', 'ghost',
                                 'rock', 'door', 'skull', 'tile', 'bat', 'bird', 'bug', 'rocket', 'fruit', 'love',
                                 'power',
                                 'rose', 'bat', 'cursor', 'flag', 'hand', 'key', 'sun', 'stump', 'star', 'moon', 'fungi', 'ufo',
                                 'reed', 'cash',
                                 'ladder', 'fear', 'door', 'bubble', 'dust', 'cog', 'flower', 'cup', 'fungus',
                                 'box', 'shirt', 'tree',
                                 'castle', 'skull_map', 'medusa', 'fir-tree', 'leaf', 'trash', 'whitecircle', 'violet', 'mount_map', 'snow_map',
                                 'ring'
                                 )
