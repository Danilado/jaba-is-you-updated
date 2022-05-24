from typing import List

import pygame

from classes.objects import Object
from utils import get_pressed_direction


class MoveCursor:
    def __init__(self):
        self.turning_side = -1
        self.levels = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.reference_point = ('moon', 'skull', 'pillar', 'pumpkin', 'flower',
                                'spike', 'jelly', 'dot', 'leaf', 'tree', 'blossom')
        self.some_obj = ('line', 'square')
        self.blocks = (*self.levels, *self.reference_point)
        self.last_time = 0

    def move(self, matrix: List[List[List[Object]]]):
        # TODO by quswadress: split move_right, move_left, move_up, move_down into this method.
        if pygame.time.get_ticks() - self.last_time > 75:
            self.last_time = pygame.time.get_ticks()
            for i, line in enumerate(matrix):
                for j, cell in enumerate(line):
                    for k, element in enumerate(cell):
                        element.x = j
                        element.y = i
                        element.movement.start_x_pixel = element.xpx
                        element.movement.start_y_pixel = element.ypx
                        element.movement.x_pixel_delta = element.movement.y_pixel_delta = 0
            if self.turning_side == 0:
                self.move_right(matrix)
            if self.turning_side == 1:
                self.move_up(matrix)
            if self.turning_side == 2:
                self.move_left(matrix)
            if self.turning_side == 3:
                self.move_down(matrix)

    def move_up(self, matrix: List[List[List[Object]]]):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i - 1][j]) != 0 and matrix[i - 1][j][0].name.split("_")[0] != 'gate' and\
                            (matrix[i - 1][j][0].name.split("_")[0] in self.some_obj or
                             matrix[i - 1][j][-1].name.split("_")[0] in self.blocks or
                             matrix[i - 1][j][-1].name.split("_")[-1] == 'teeth'):
                        matrix[i - 1][j].append(element)
                        matrix[i - 1][j][-1].movement.start_x_pixel, matrix[i - 1][j][-1].movement.start_y_pixel = \
                            matrix[i - 1][j][-1].xpx, matrix[i - 1][j][-1].ypx
                        matrix[i - 1][j][-1].y -= 1
                        matrix[i - 1][j][-1].animation.position = (matrix[i - 1][j][-1].xpx, matrix[i - 1][j][-1].ypx)
                        matrix[i - 1][j][-1].movement.x_pixel_delta, matrix[i - 1][j][-1].movement.y_pixel_delta = \
                            matrix[i - 1][j][-1].xpx - matrix[i - 1][j][-1].movement.start_x_pixel, \
                            matrix[i - 1][j][-1].ypx - matrix[i - 1][j][-1].movement.start_y_pixel
                        matrix[i - 1][j][-1].movement.rerun(0.05)
                        cell.pop(k)

    def move_down(self, matrix: List[List[List[Object]]]):
        num_el = None
        x = None
        y = None
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i < 17 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i + 1][j]) != 0 and matrix[i + 1][j][0].name.split("_")[0] != 'gate' and\
                            (matrix[i + 1][j][0].name.split("_")[0] in self.some_obj or
                             matrix[i + 1][j][-1].name.split("_")[0] in self.blocks or
                             matrix[i + 1][j][-1].name.split("_")[-1] == 'teeth'):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x + 1][y].append(matrix[x][y][num_el])
            matrix[x + 1][y][-1].movement.start_x_pixel, matrix[x + 1][y][-1].movement.start_y_pixel = \
                matrix[x + 1][y][-1].xpx, matrix[x + 1][y][-1].ypx
            matrix[x + 1][y][-1].y += 1
            matrix[x + 1][y][-1].animation.position = (matrix[x + 1][y][-1].xpx, matrix[x + 1][y][-1].ypx)
            matrix[x + 1][y][-1].movement.x_pixel_delta, matrix[x + 1][y][-1].movement.y_pixel_delta = \
                matrix[x + 1][y][-1].xpx-matrix[x + 1][y][-1].movement.start_x_pixel, \
                matrix[x + 1][y][-1].ypx-matrix[x + 1][y][-1].movement.start_y_pixel
            matrix[x + 1][y][-1].movement.rerun(0.05)
            matrix[x][y].pop(num_el)

    def move_left(self, matrix: List[List[List[Object]]]):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j - 1]) != 0 and matrix[i][j - 1][0].name.split("_")[0] != 'gate' and\
                            (matrix[i][j - 1][0].name.split("_")[0] in self.some_obj or
                             matrix[i][j - 1][-1].name.split("_")[0] in self.blocks or
                             matrix[i][j - 1][-1].name.split("_")[-1] == 'teeth'):
                        matrix[i][j - 1].append(element)
                        matrix[i][j - 1][-1].movement.start_x_pixel, matrix[i][j - 1][-1].movement.start_y_pixel = \
                            matrix[i][j - 1][-1].animation.position
                        matrix[i][j - 1][-1].x -= 1
                        matrix[i][j - 1][-1].animation.position = (matrix[i][j - 1][-1].xpx, matrix[i][j - 1][-1].ypx)
                        matrix[i][j - 1][-1].movement.x_pixel_delta, matrix[i][j - 1][-1].movement.y_pixel_delta = \
                            matrix[i][j - 1][-1].xpx-matrix[i][j - 1][-1].movement.start_x_pixel, \
                            matrix[i][j - 1][-1].ypx-matrix[i][j - 1][-1].movement.start_y_pixel
                        matrix[i][j - 1][-1].movement.rerun(0.05)
                        cell.pop(k)

    def move_right(self, matrix: List[List[List[Object]]]):
        num_el = None
        x = None
        y = None

        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j < 31 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j + 1]) != 0 and matrix[i][j + 1][0].name.split("_")[0] != 'gate' and\
                            (matrix[i][j + 1][0].name.split("_")[0] in self.some_obj or
                             matrix[i][j + 1][-1].name.split("_")[0] in self.blocks or
                             matrix[i][j + 1][-1].name.split("_")[-1] == 'teeth'):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x][y + 1].append(matrix[x][y][num_el])
            matrix[x][y + 1][-1].movement.start_x_pixel, matrix[x][y + 1][-1].movement.start_y_pixel = \
                matrix[x][y + 1][-1].animation.position
            matrix[x][y + 1][-1].x += 1
            matrix[x][y + 1][-1].animation.position = matrix[x][y + 1][-1].xpx, matrix[x][y + 1][-1].ypx
            matrix[x][y + 1][-1].movement.x_pixel_delta, matrix[x][y + 1][-1].movement.y_pixel_delta = \
                matrix[x][y + 1][-1].xpx-matrix[x][y + 1][-1].movement.start_x_pixel, \
                matrix[x][y + 1][-1].ypx-matrix[x][y + 1][-1].movement.start_y_pixel
            matrix[x][y + 1][-1].movement.rerun(0.05)
            matrix[x][y].pop(num_el)

    def check_events(self):
        """Метод обработки событий"""
        self.turning_side = get_pressed_direction()

"AdNV4mG3SRdeskVlkjqi3DxMPi8JaHZs63SGvfaCI2X7qV0cftz65cov6Cx5VQJGJwFMaSaZEFU5C6dy1RbeJYwLLJCl5CgabE4ypgD8QMtwEET0NU2UtelJj1tDky3zKAW6EA2I6OT4ubdYVZ1ZbhqDUuRshDTVW3ult4kmYiYt2qPF10iBjHYlE4Rn1EEhhZtF4VmUROhrJ4o9OsGaSOZvKu4oVblkXUn5TOFypUMq6MVAPfiDCB3DC0RQrHiZ0Iv7mtmQjtExOu0ctlzi27UGdH3zP5tJggZkfqWv68hoDlVdxMwU7kAcKLj11gLokVCdxYsnNkJUYxm4SHgOs4l1gEpuSvQSBcjMcaHPxyBEnOZB7YNjlhFZo1mtj26npyBnOgvXrFEFQMvKvwz6oLa2RP6Cw79TSTex5ijl8kUuVvjlV78DykJtCDqHBnY1I67EAllrA8KbeSfRAv0MQO5zD0yo6B3l1oht7pElRzze7yPwTkSYrOz76Fioo4ODUqxA8IRpXCg0cebFGJE6YV9cNz0IKDq7UYcVAwKfarSzmQohJ5WxQLgntWAadLPVroNkyTNJzy612MLyP5l5i8yboJOYOmdIp0fGkX9gBpGOBH29zCZP64b2ZtzHaM3kt9SMJft6bPB97LyYgRsqxhZKnc5fSKtEyVI1GV0GOLj09stbeNSkjih3Rvcm60HpiD7PVFrlBkv4JabFtH92McDPiDB0HLxpAbi1ThuOoUzU9lXY0KlzEXAFEaBBcflpTBbTxDTnmlcxv7qX5y5a3IsrhMkinD3zWNfguAFODHPFaUhIbrbSyIn7wWxH6Pazb82cSc2dz3KngNDtwJPX5FzkKQYAkg80gEq2EdeTkxNY6Awu43qwkFUuNLMecUSCbp7UvIeMd31awbzi5ccyknk5RTL0YdPJzUy8c8Peumc8cJPFY77qW4GDLb43UmBXspmjboBa3kVmc3vGEkt8l7GsXG1q7y5C7WktmPphhw2iX3fV49vuLbqPD7nDLOdmZ2TkO0EUnZJQuQIt0VuCGhG8DAV6DURWyD2DvYpfhfX7oEU6JVxht0LN88htbc0zkJ64gcYqoQNIJsb9yZbuLkmeSHRp2XOT08jeel6CMpVqssfG4h9Hw4LNIJVJNQRw1VmNn92UoMcUdFrxV4n6ONYe9T1VceXFFnh1Q9QwWAm0AHt0NYKe0Pgw7aQHwArmyeKdt5TPsHI5k83FDsI5q6hLJm8EkwUJRZDrP5iYffDitpGLtgh8BLfaJEXnSwMsrWCaioXD0VxhsqdgeuhQtAvu6mRZTIcGaIvAosJgicuB5QFgJ50CtcFqX1vMZLgPE56ptfqEDvO2NnWezUko2kyoFfxxJVqiuFpaohvlCSS1rm4ejpYeNjcOMb9gjSeb69pGziTz7OxN2XpKV3JpEt9LhzLmxhnypfJvR14ZRwKsT75HBkj5O92V5ZEzmCbXS6i4FFQ3bKRWuBy4tL5iIiYZou4zm2OFwooRIqRhRQZzSS2vL0IGkwGC3BouBgbSOshyoDUpRUHvwtxWuPbZ5gjB44hHe8bl5GJ4n4NWF1BYjDHg83ReF0tmMRIJZVRkjBJq3nf6APBH0yP8BjzUeyN3XEbBEogQAlMnjVZt8nqCXSJzZc1sQ5UCZ9yvQvgia7l5dvguF4ThsY0Yguif4GPeLb24lxqcdDNvQqXHK7QSWR7IEmAguqflcW3NBNfokuPwgr1pgZIQzn0w6cCKhrEZCRK5HcSuzePOOuY1yVyQXGXnLEJgfmeTPACee6io1JWuYjMtgo1tWt7i7qgQzNFtqkvGETB8lv13Bnd0DEP73LcE6UbWdaBIisw7nQcHqNxUsBbMyn3tEguCtkWZWi4ZfC4RwVxWLkO2PR3Wl3T6p6wMItjdh0GRISBZbyq00g3OvBWnyC8OvEWvOH3m6qryhKSmrKTZNVA80cD7IE406lBj5TJGGl5sS1oKNfgqiPVBa0qkOQiz876fFcIGgmpguk7ScdPm8T1UYGEe5ooA7aryDxyr2eyne9fj8bKylFwQ59FPiLPWl1Q5seFCNeVDzMHlM9sO9qHLAQsAx21m4tnAW742bCfJSZJHQAyKiocOZtsURrK7I440cuuH3ks4xGk0S17H28WnYv8lKPC9W0a4AlP0NKpVhwRKq2FRF2kZIYb3tMrDV8V3rLFmt915iaa6Kp24IfvNKlnaft64a8IGjzrbS3IXMMp5nEn8yiFQczymJaO5Xy6cr0Tvl9PMwlKCzvwxNLwvSc31XwLo5yGcZ4ABVLcZjRdpc9V2kZjSJl0IzenPLzPB5qcu7J48w4QecomtO1yFYHDQSBwgOFz7IyExh9FiZ1d8sEWFSXVyNNsNm5xRbJqrNfF0mx4dLcDrTZglR5JuT5gFkjpPfVp9x3hi5s7PhoXpHhXxOaIKgJaklGqULWxgH0U0h7Cmb0Tw4kGn3IQkiJmaJ4lKMdkP9Tx9Igs0k6WIjHutEwY6MEwpJvXM9oqHZbUqed8GrHNetF7oKPDbTaK1TzaOovrQoz5N1Q3xsPpky2tYBFWuUvBTwCdO7GfdnSWnXFv7Zgyhfgyv3wBxGayd67ltG5m306dJvbrv4mlVYzCp6PvT9euKyRu7war8ACv1HyHvxZ99cdtmXCXQAmg31uFBTC2QhZatULgKvabBFe6w65TvfFZeJdipMTgVhre1ZCtendSPnJr6f3lYwjcCeIgEhLczvLHuHBP5imS3tyvoT7xyrmW6zIHE2q1ci7ryFZHqo556OfZLgqMqSvxXTlMqVsppS7XuwE4sYgDz21Zo6wzVBhecKu3G39BrJtPsGOYFjVwlZg1aVLD2V6bUDRXR6sQQgFGWgWqAzuXPi5cPA3hWpbxbKuSCOrv8uMXJorP4esOtVpXszcxa2rJOjoyucf0khNNwjcu73dal55CSIypr9moWFCQJQdOLAdSxg0nAFwx97cNctlGGZdDNWyydZAzIjNNvcwXlo84IVtOunFbhB59TiJd8r3nOOwwahA3DZJrMjduS8HvRBQy68lu1GgW52bUu9pmzW8JlPsmNiTQbDw5ockUQr9W5gn2imI3YG0WFgrECPI7To17QUjO9ujXNZpq516r6PtgqtdbxGX1hFD5ajfkTO3vQaAMCKSqaNdCK92Wyf8ZVBkXNoQKsXfcaGxPZlmAoLICWi9uZxXAbvJX7QNvLrDw0PxopU8RNRPF3tiQMg4mMfWYzq80Q4GBKcZUL8Oa0R71Oi6X9TNWQqeATUa3QcKhI4kbLu6kmtKxtUcZFAEn3xCCbNq63iJgEmJo3vbNCHBeRKXSCqNCJWD5e9skaA5S4VUpjQiWtxu4QscGIW80udcw0T6O43wLZY4uSK9YmEmzeA5UoiRDA7MKCuTevx6E3j63cm8kkG5AsjCzJspN0EsYumbTmeMFrc652mHhjKrC9UFrjq2u5Rvi8V6iDTK6V1aSousa6GDZpnvAMi4hJGb8ontvQ4wh2nh5lpPnU5tMIWmbTXlOXCrniWGPWjekhDbTo2AObrsOJeat2YHiPhvSijrssXzqQdV6goRIm4jcIhF9dQDlB7w03EDazmnL3XNjMl1RWuvpH0zJfBSflpkkDmWcJSJyE3qJRPCr93cWXAri2Ac8wYT5Qgaa7qMoMsXu5q2jKdrTFxn37ODqgwrc6BBu7SQV2sna4JUDePoAv4vozji6u7oiZQiKSRT9KWIygfPXJpIvsvFYLlHBvKb3ZGrD1jXBT15eTkx4DAVqp52sBMTgJDl1rJAiwq9eARDx66NxFSAlmJjSkZ7Ncc6OJ2ECNrzGI3HO2ZGHkBOlkvBGQlWsluWFB1Mp5sHckqZl2jJ5OfiUxxPbozQXtd4eN3peTc4AeIpq3fqalwbfvBPB9Jq0w7ErOUQylUz5w7NSYWaGvfUrtZjbLTEdrX2M49AQttyOllg6g6ywBPqKAabHI1B6viB0hTkCKZXVOqr2l9mgnEsL8Z0gtTCl4ADlLm2uXAjaUnlONU7c2Fmy3SbXc366Zl7QSibg8N36pnvwOHsWOyQ19KkxCmVUjG4dLiO3ZeWYjXNLlp4tWduK19FslVLk0r3hXYHe7WR5XOKhY82BLwhOJLvGyMWF0pusLGywcybZdzDV0puVcW4I8mTbhjmmAw5sbjezJ6hsaYseWx86ebx0jnXkuw9r4VdFlrIV6MokfKG3cZc3DZxhwTv6WgiFIBLfcKmKHNy8xtEVkT0KKoMSyYhhPT4PxujDS3tcHe1bWicT4s1jQMV6VAq0c69yAbjxd1xE9HD4tAwHQMpfhWMXf4DWXYFEkbPDJHGeQ4yKZ4LxXWRMC7zEi12Ib0C9AEeHur1A5qk5RvC5tk7Z7GtCDJweGOafxM1mFghPtRHI1GQcwv6XL40F5eS8v9o8Mz1cOCpfq6CDXOL7XT8haSPYS2ZMuILDhGR64Lui9MJkbLxDkh1bEdMsyFsZw8ip9ILjafVDIwncgb24fe2GmPBzWOqXgn5yLvmovBr84gFDxXc3I0746C4OA3gdvFpHxL1Iz1f1YatJ6U5tXXw2ScztT6srx0SrTrU5zE6qrd3LhansragEEJbfsptU09FT5m6Ll8ApzrEFMyAyGpOAScyu3FmmQf6pZ5ijSB6jd3fkcOstGl9RCip9fGH0kbP6OwXxvopm0YKx69FdEumQFXulRzoIII4p5yAmPH1qBABxWF4pEkXUoMulxvELtx7K10J7QjVPMg1faaE9IAaWUNnTFabzlj6tTmUDLk2HE0mQw45jWTPrDODZlQKdOQ9z7Zb7BhCAxxyfjsdBa608ErQwQcgq93v9TGT9iFgWD44tEkFRj1ON2GJuPxp6vlZDEd9kFTP1lDSwOc8itT75KHEyiAH0V5V7QRGjYbwfozGsr44yp1BPeBTFlox9yitd8dZAaBAfkKtZlDOg8NJ4cgiEODOM9zqUdkR4RuWvnoNHXgCFa3tDCrfG1jWSGsYdDNFdeV9u1w3IrQFB8qsizxgRVDd9VXSziejl3ezQyeaAVBiQLpYz5L8EghmtOO5UCUv094CZCIFNhJglBHhxHPxhfIkFxGI5mzLHj41a2xmM5mG6mXVg9ZpuUwtZTUfNivUNDiCcW3eKt4B8N4rGFtoaOK7czJKKYA3S4oHR69FxTSjPNHuRNOPwor2Eppgj9xQJQaZUEDHKFa3j5EKKhsgSyDcJp60xSwlThCueVECbgJ7T671nEQQPJcKo18oUVhxX2vapxfvvwksFiDeqkQHPZ3ijnekyVQ2fTW65npRM1PB7yopPbYzTRF250O2wLdCauRlYf08q1rQkpbk"