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

"sSgqLDGOKN3j99YWSYEDXECBikiyLhNO92wO8cJ7SKl2vIamGkhGflHC8gX3RFSSjv4Mw0NXx5SNFj06J70oYSQQ3x0uzokNPbqbvsH1tip20y7WDpA2SfRsVJf51eQZNclv5pgHCf1OrPjjGs1tlcAyBENANAisMQ35LWQDrJByBH2s8FwasY1n5rN6ZlJk1d1mcBwkvOxL2tey8qxYusE7f6pI7wBAHM4u2SSdqTE8APQf9mfzyzqGzz6dIAhrgWJKPaF4CZ2Piy5jvSPJO6gC2JVzkK6b6K0mropMxMWMUMiVExozStAJSduIN0S1NQmLcwQS0ad6DAAskkvJAITjo3J493vTMgZsAvHTPFiMfgD5aSx6HKnIjvl9i9E24lpWTr2tZIbhbq5HO2BgMc4GJmjHJluR1iCtwt6BLDYVeOIh2Q7C7wygFz8Cv7kYprrbvRG1hvhp37BVB4LTQMV4WAiRxklUFqrz5EKP3jK5Phb2fxj8zKAuhLFB1aHZaxMrtE3o8TWL7AjTbTaV4EmZPM2LHnF7rNwjdCy2srR6l17Kp46gE7daPW3E7MiEfXcYjQR0vQgwU4FH2t8o2yd2mgStkQcSypEFCDFvD4sZdioFiORbFtyBV5X8uz8LPKxRVSM0XsX15SwmHuEi8yhHd6hVn6kUyRqW7WQy8xMz9vmcS8u1W9OJj22YMgBESAHtsOkLGlTQjNXDoG7WalylVW0PD48e24AyeOFGjVZdV4NUuj334ybU6JNuaVTryKqh9drPeaqCMf3Hn583WMXOk1ztlJvC2x4lF5RXhlVfV3X1q68WTCAVhY91WUDQwKm5kEixTNfsKUupKjf3Xm2saP9SYQGeyMUYxhVXQumWoQoX2cmJzpQF9OSbziwHEpwACLGwBgX652y9YwYFSHlYbUMsFz13T8hkolAOQkMffo5aZUdYefumVTzRO7z2kmA31hwdGgdcXqBmeT5UXnahdoRIAz2r8y1HOceS3krmk0C7Ir6UVP8JhTYFWrg9WGA7taOTR89WZjjaZdH3OZ6opPcZ0DNTBqnOhLURrJ0qmtBnHzsP5ULPdtClgXMXb0nrFCgZLCsOhur0GrlO7A9X2PhDD8ak3htB7dIjVLpPigTKXtOlzXWrCbZWu0KO7G5aoMI8tmExZAZ1V0OVg5b53Xoj2mw8eylBJSqwGtBGGrkxrP7A9PN157lmcBwq5QY1St6gIjnzFEjEOO3mvzz4KLBCMA7gELz7yYlCTTviS3t1JDU5Xw7BVHeVvVXcQAx3JeNNVa59pEkPblL6ptXsTxwVn2u3EtmvOxWRgV21QgvU6l0fFJaAxhQUhhLVOTpGoJuGUMkgvngR0Z7O9wxJWztthGbos9anoYQaOOgXFworSwPww9qEOMr9LWE0gDw4gc9UWC53dxjt5QhcDXhahthi9X4SVVFr8W1xq7U2KKnRFPHrhd4YOmY1rb2eB3vBEhnLa2CShPSH2WUwSgLHhCRMqMKLZIFtuW6pEYYznknYM65pXqOxRAK1Mfuwf9EtPOfLgmiyAmxBgnAZWF0WIG5yyC3eqaMBqQgkTDEfnsf1hUo2c1z6wP9iSSzb189PlBXdUGwg5mzhPNg37cwzX9LzkqUNWlD752gUqSeReIdmBgmrvaOyVRYOeabXu1biPnqFhX9z4BRqxUZEPxEpx4CAMXBQe1aMuPADiYjn1WQ8xfAw0k25Ltq1mQyZ5AIQNTDEiiZSY7peGI4ar0dDfCu5joH4PuJZMglBrDWXpFFKmq1jn8phLHdVGjt0GpczHDztAke40cpvQDdRGDj8txCOGd6X7KlKd46rSrN8CNL9I1bMhJjHhQtn6Jsq4HmwQJKrifn9lY2EnRtQ9QDXy9AmvSeoNEUlFQ5ueMtvzpaEAHKMTnjML2OA2i4HBf8rIwubKTNcIpSmSyqA4KKjIFDfCjZ7mgfFZhO0NgVJtYSlsus4T"