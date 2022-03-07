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

LETTERS: Final[Sequence[str]] = ('ring', 'words/a', 'skull_map', 'trash', 'mount_map', 'medusa', 'whitecircle',
                                 'fir-tree', 'snow_map', 'castle', 'words/b', 'words/c', 'words/d', 'words/e',
                                 'words/f', 'words/g', 'words/h', 'words/i', 'words/l'
                                 )

OBJECTS: Final[Sequence[str]] = (*TEXT_ONLY, *PIPES, *LETTERS, 'cake', 'fire', 'ghost',
                                 'rock', 'door', 'skull', 'tile', 'bat', 'bird', 'bug',
                                 'rocket', 'fruit', 'love', 'power', 'rose', 'bat', 'cursor',
                                 'flag', 'hand', 'key', 'sun', 'stump', 'star', 'moon', 'fungi',
                                 'ufo', 'reed', 'cash', 'ladder', 'fear', 'door', 'bubble', 'dust',
                                 'cog', 'flower', 'cup', 'fungus', 'box', 'shirt', 'tree', 'leaf',
                                 'violet',
                                 )

NOUNS = [
    'algaе', 'all', 'anni', 'arrow', 'baba', 'badbad', 'banana', 'bat', 'bed', 'bee', 'belt', 'bird', 'blob', 'blossom',
    'boat', 'boba', 'bog', 'bolt', 'bomb', 'book', 'bottle', 'box', 'brick', 'bubble', 'bucket', 'bug', 'burger',
    'cake',
    'car', 'cart', 'cash', 'cat', 'chair', 'cheese', 'circle', 'cliff', 'clock', 'cloud', 'cog', 'crab', 'crystal',
    'cup',
    'cursor', 'dog', 'donut', 'door', 'door2', 'dot', 'drink', 'drum', 'dust', 'ear', 'edge', 'egg', 'empty', 'error',
    'eye', 'fence', 'fire', 'fish', 'flag', 'flower', 'fofo', 'foliage', 'foot', 'fort', 'frog', 'fruit', 'fungi',
    'fungus',
    'gate', 'gem', 'ghost', 'grass', 'group', 'guitar', 'hand', 'hedge', 'hihat', 'house', 'husk', 'husks', 'ice',
    'image',
    'it', 'jelly', 'jiji', 'keke', 'key', 'knight', 'ladder', 'lamp', 'lava', 'leaf', 'level', 'lever', 'lift', 'lily',
    'line', 'lizard', 'lock', 'love', 'letters', 'me', 'mirror', 'monitor', 'monster', 'moon', 'nose', 'orb', 'pants',
    'pawn', 'piano', 'pillar', 'pipe', 'pixel', 'pizza', 'plane', 'planet', 'plank', 'potato', 'pumpkin', 'rain',
    'reed',
    'ring', 'road', 'robot', 'rock', 'rocket', 'rose', 'rubble', 'sax', 'seastar', 'seed', 'shell', 'shirt', 'shovel',
    'sign', 'skull', 'spike', 'sprout', 'square', 'star', 'statue', 'stick', 'stump', 'sun', 'sword', 'table', 'teeth',
    'text', 'tile', 'tower', 'track', 'train', 'trash', 'tree', 'trees', 'triangle', 'trumpet', 'turnip', 'turtle',
    'ufo', 'vase', 'vine', 'wall', 'water', 'what', 'wind', 'worm'
]

OPERATORS = [
    'and', 'eat', 'facing', 'fear', 'follow', 'has', 'idle', 'is', 'lonely', 'make', 'mimic', 'near', 'never', 'not',
    'on', 'operator', 'play', 'powered', 'seldom', 'sharp', 'without', 'write'
]

PROPERTIES = [
    '3d', 'auto', 'back', 'best', 'bonus', 'boom', 'broken', 'chill', 'crash', 'rosy', 'pink', 'red', 'orange',
    'yellow', 'lime', 'green', 'cyan', 'blue', 'purple', 'brown', 'black', 'black', 'black', 'grey', 'silver', 'white',
    'defeat', 'return', 'done', 'directions', 'end', 'fall', 'float', 'hide', 'hold', 'hot', 'locked', 'melt',
    'more', 'move', 'nudge', 'open', 'party', 'pet', 'phantom', 'power', 'pull', 'push', 'reverse', 'revert', 'sad',
    'safe', 'scary', 'select', 'shift', 'shut', 'sink', 'sleep', 'stick', 'still', 'stop', 'swap', 'tele', 'turn',
    'weak', 'win', 'wonder', 'word', 'you', 'you2'
]
