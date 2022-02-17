import enum


@enum.unique
class GameState(enum.Enum):
    """Перечисление изменений которые может сделать GameStrategy в GameContext"""
    stop = enum.auto()  #: Остановить игру
    switch = enum.auto()  #: Сменить стратегию
    back = enum.auto()  #: Вернуть прошлую стратегию
    flip = enum.auto()  #: Нарисовать на экране
