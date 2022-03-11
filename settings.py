from typing import Final, Tuple, Sequence

DEBUG: bool = True

RESOLUTION: Final[Tuple[int, int]] = (1600, 900)  # 32x18
SHOW_GRID: Final[bool] = True
FRAMES_PER_SECOND: Final[int] = 60

TEXT_ONLY = [
    '0', '1', '2', '3', '3d', '4', '5', '6', '7', '8', '9', 'a', 'ab', 'above',
    'all', 'and', 'auto', 'b', 'ba', 'back', 'below', 'besideleft', 'besideright',
    'best', 'black', 'blue', 'bog', 'bonus', 'boom', 'broken', 'brown',
    'c', 'chill', 'cyan', 'd', 'defeat', 'deturn', 'done', 'down',
    'e', 'eat', 'empty', 'end', 'f', 'facing', 'fall', 'falldown', 'fallleft',
    'fallright', 'fallup', 'fear', 'feeling', 'flat', 'float', 'follow', 'g', 'green',
    'grey', 'group', 'group2', 'group3', 'h', 'has', 'hide', 'hot', 'i', 'idle',
    'is', 'j', 'k', 'l', 'left', 'level', 'lime', 'lockeddown', 'lockedleft',
    'lockedright', 'lockedup', 'lonely', 'm', 'make', 'melt', 'mimic', 'more', 'move',
    'n', 'near', 'nextto', 'not', 'nudgedown', 'nudgeleft', 'nudgeright', 'nudgeup',
    'o', 'often', 'on', 'open', 'orange', 'p', 'p1', 'p2', 'party', 'pet', 'phantom', 'pink',
    'play', 'power', 'power2', 'power3', 'powered', 'powered2', 'powered3', 'pull',
    'purple', 'push', 'q', 'r', 'red', 'reverse', 'revert', 'right', 'rosy', 's', 'sad', 'safe',
    'scary', 'seeing', 'seldom', 'select', 'sharp', 'shift', 'shut', 'silver', 'sink',
    'sleep', 'still', 'stop', 'swap', 't', 'tele', 'turn', 'u', 'up', 'v', 'w', 'weak',
    'white', 'win', 'without', 'wonder', 'word', 'write', 'x', 'y', 'yellow', 'you', 'you2', 'z'
]

SPRITE_ONLY = [
    'blossom', 'default', 'error', 'ico', 'nope', 'seastar', 'tree2',
]

STICKY = [
    'lava', 'wall', 'cloud', 'brick', 'plank', 'rubble', 'hedge', 'cliff', 'grass', 'ice', 'line', 'road', 'track', 'water'
]

OBJECTS = [*TEXT_ONLY, 'algae', 'arrow', 'baba', 'badbad', 'banana', 'bat', 'bed', 'bee', 'belt',
           'bird', 'blob', 'blossom', 'boat', 'boba', 'bolt', 'bomb', 'book', 'bottle', 'box', 'brick',
           'bubble', 'bucket', 'bug', 'burger', 'cake', 'car', 'cart', 'cash', 'cat', 'chair',
           'cheese', 'circle', 'cliff', 'clock', 'cloud', 'cog', 'crab', 'crystal', 'cup', 'cursor', 'default',
           'dog', 'donut', 'door', 'dot', 'drink', 'drum', 'dust', 'ear', 'egg', 'error', 'eye', 'fence', 'fire',
           'fish', 'flag', 'flower', 'fofo', 'foliage', 'foot', 'fort', 'jaba', 'fruit', 'fungi', 'fungus', 'gate',
           'gem', 'ghost', 'grass', 'guitar', 'hand', 'hedge', 'hihat', 'house', 'husk', 'husks', 'ice',
           'it', 'jelly', 'jiji', 'keke', 'key', 'knight', 'lava', 'ladder', 'lamp', 'leaf', 'lever', 'lift', 'lily',
           'line', 'lizard', 'lock', 'love', 'me', 'mirror', 'monitor', 'monster', 'moon', 'nose', 'orb',
           'pants', 'pawn', 'piano', 'pillar', 'pipe', 'pixel', 'pizza', 'plane', 'planet', 'plank', 'potato',
           'pumpkin', 'reed', 'ring', 'road', 'robot', 'rock', 'rocket', 'rose', 'rubble', 'sax', 'seed',
           'shell', 'shirt', 'shovel', 'sign', 'skull', 'spike', 'sprout', 'square', 'star', 'statue', 'stick', 'stump',
           'sun', 'sword', 'table', 'teeth', 'tile', 'tower', 'track', 'train', 'tree', 'tree2', 'trees', 'triangle',
           'trumpet', 'turnip', 'turtle', 'ufo', 'vase', 'vine', 'wall', 'water', 'what', 'wind', 'worm'
           ]

# Povelitel's tools

NOUNS = [
    'algaе', 'all', 'anni', 'arrow', 'baba', 'badbad', 'banana', 'bat', 'bed', 'bee', 'belt', 'bird', 'blob', 'blossom',
    'boat', 'boba', 'bog', 'bolt', 'bomb', 'book', 'bottle', 'box', 'brick', 'bubble', 'bucket', 'bug', 'burger', 'cake',
    'car', 'cart', 'cash', 'cat', 'chair', 'cheese', 'circle', 'cliff', 'clock', 'cloud', 'cog', 'crab', 'crystal', 'cup',
    'cursor', 'dog', 'donut', 'door', 'door2', 'dot', 'drink', 'drum', 'dust', 'ear', 'edge', 'egg', 'empty', 'error',
    'eye', 'fence', 'fire', 'fish', 'flag', 'flower', 'fofo', 'foliage', 'foot', 'fort', 'frog', 'fruit', 'fungi', 'fungus',
    'gate', 'gem', 'ghost', 'grass', 'group', 'guitar', 'hand', 'hedge', 'hihat', 'house', 'husk', 'husks', 'ice', 'image',
    'it', 'jaba', 'jelly', 'jiji', 'keke', 'key', 'knight', 'ladder', 'lamp', 'lava', 'leaf', 'level', 'lever', 'lift', 'lily',
    'line', 'lizard', 'lock', 'love', 'letters', 'me', 'mirror', 'monitor', 'monster', 'moon', 'nose', 'orb', 'pants',
    'pawn', 'piano', 'pillar', 'pipe', 'pixel', 'pizza', 'plane', 'planet', 'plank', 'potato', 'pumpkin', 'rain', 'reed',
    'ring', 'road', 'robot', 'rock', 'rocket', 'rose', 'rubble', 'sax', 'seastar', 'seed', 'shell', 'shirt', 'shovel',
    'sign', 'skull', 'spike', 'sprout', 'square', 'star', 'statue', 'stick', 'stump', 'sun', 'sword', 'table', 'teeth',
    'text', 'tile', 'tower', 'track', 'train', 'trash', 'tree', 'trees', 'triangle', 'trumpet', 'turnip', 'turtle',
    'ufo', 'vase', 'vine', 'wall', 'water', 'what', 'wind', 'worm''algaе', 'all', 'anni', 'arrow', 'baba', 'badbad',
    'banana', 'bat', 'bed', 'bee', 'belt', 'bird', 'blob', 'blossom', 'boat', 'boba', 'bog', 'bolt', 'bomb', 'book',
    'bottle', 'box', 'brick', 'bubble', 'bucket', 'bug', 'burger', 'cake', 'car', 'cart', 'cash', 'cat', 'chair', 'cheese', 'circle',
    'cliff', 'clock', 'cloud', 'cog', 'crab', 'crystal', 'cup', 'cursor', 'dog', 'donut', 'door', 'door2', 'dot', 'drink',
    'drum', 'dust', 'ear', 'edge', 'egg', 'empty', 'error', 'eye', 'fence', 'fire', 'fish', 'flag', 'flower', 'fofo',
    'foliage', 'foot', 'fort', 'frog', 'fruit', 'fungi', 'fungus', 'gate', 'gem', 'ghost', 'grass', 'group', 'guitar',
    'hand', 'hedge', 'hihat', 'house', 'husk', 'husks', 'ice', 'image', 'it', 'jelly', 'jiji', 'keke', 'key', 'knight',
    'ladder', 'lamp', 'lava', 'leaf', 'level', 'lever', 'lift', 'lily', 'line', 'lizard', 'lock', 'love', 'letters', 'me',
    'mirror', 'monitor', 'monster', 'moon', 'nose', 'orb', 'pants', 'pawn', 'piano', 'pillar', 'pipe', 'pixel', 'pizza',
    'plane', 'planet', 'plank', 'potato', 'pumpkin', 'rain', 'reed', 'ring', 'road', 'robot', 'rock', 'rocket', 'rose',
    'rubble', 'sax', 'seastar', 'seed', 'shell', 'shirt', 'shovel', 'sign', 'skull', 'spike', 'sprout', 'square', 'star',
    'statue', 'stick', 'stump', 'sun', 'sword', 'table', 'teeth', 'text', 'tile', 'tower', 'track', 'train', 'trash', 'tree',
    'trees', 'triangle', 'trumpet', 'turnip', 'turtle', 'ufo', 'vase', 'vine', 'wall', 'water', 'what', 'wind', 'worm'
]

OPERATORS = [
    'and', 'eat', 'facing', 'fear', 'follow', 'has', 'idle', 'is', 'lonely',
    'make', 'mimic', 'near', 'never', 'not', 'on', 'operator', 'play',
    'powered', 'seldom', 'sharp', 'without', 'write'
]


PROPERTIES = [
    '3d', 'auto', 'back', 'best', 'bonus', 'boom', 'broken', 'chill', 'crash', 'rosy', 'pink', 'red', 'orange',
    'yellow', 'lime', 'green', 'cyan', 'blue', 'purple', 'brown', 'black', 'black', 'black', 'grey', 'silver', 'white',
    'defeat', 'return', 'done', 'up', 'left', 'down', 'right' 'end', 'fall', 'float', 'hide', 'hold', 'hot',
    'lockeddown', 'lockedup', 'lockedleft', 'lockedright', 'melt',
    'more', 'move', 'nudge', 'open', 'party', 'pet', 'phantom', 'power', 'pull', 'push', 'reverse', 'revert', 'sad',
    'safe', 'scary', 'select', 'shift', 'shut', 'sink', 'sleep', 'stick', 'still', 'stop', 'swap', 'tele', 'turn',
    'weak', 'win', 'wonder', 'word', 'you', 'you2'
]
