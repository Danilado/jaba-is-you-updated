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
