from typing import Final, Literal, Dict

import pygame


def my_deepcopy(arr):
    """Полное копирование трёхмерного массива без использования указателей

    :param arr: Исходный массив
    :type arr: list
    :return: Копия в других ячейках памяти
    :rtype: list
    """
    new_arr = []
    for val in arr:
        if isinstance(val, list):
            new_arr.append(my_deepcopy(val))
        else:
            new_arr.append(val)
    return new_arr


def get_pressed_direction() -> \
        Literal[-1, 0, 1, 2, 3]:
    """Метод обработки клавиш поворота чего-либо"""
    side_and_key: Dict[int, Literal[0, 1, 2, 3]] = {
        pygame.K_d: 0,
        pygame.K_w: 1,
        pygame.K_a: 2,
        pygame.K_s: 3
    }
    bad: Final[Literal[-1]] = -1
    turning_side: Literal[-1, 0, 1, 2, 3] = bad
    for key in side_and_key.keys():
        if pygame.key.get_pressed()[key]:
            turning_side = side_and_key[key]
            break
    return turning_side
