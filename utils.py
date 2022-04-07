import os


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


def settings_saves():
    options = []
    if os.path.exists('option_settings'):
        with open('option_settings', mode='r', encoding='utf-8') as saves:
            for param in saves:
                options.append(param.strip())
            if options[0] == 'False':
                options[0] = False
            else:
                options[0] = True
            options[1] = str(options[1])
            options[2] = float(options[2])
            options[3] = int(options[3])
            options[4] = float(options[4])
    else:
        options.append(True)
        options.append('Eng')
        options.append(1.0)
        options.append(0)
        options.append(1.0)
    return options



def language_words():
    if settings_saves()[1] == 'Ru':
        file = 'ru_words'
    else:
        file = 'eng_words'
    with open(file, mode='r', encoding='utf-8') as words_file:
        words = []
        for param in words_file:
            words.append(param.strip())
        return words
