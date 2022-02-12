import enum


@enum.unique
class GameState(enum.Enum):
    stop = enum.auto()  # Остановить игру
    switch = enum.auto()  # Сменить стратегию
    back = enum.auto()  # Вернуть прошлую стратегию
    flip = enum.auto()  # Нарисовать на экране
