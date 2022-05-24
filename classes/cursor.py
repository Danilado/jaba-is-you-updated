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

"CzTaJkwdC8XYgqinKAfkIRBrKVVc1l7PBmc39hKfjap5rgngQxEaacd8caZbiz18KCH7hVZOzeJXkauymebtIZgQyUJiHnPCdAexx1hY6F689z8KriDoRb4VEHrWsjLdRvNQ5vExvc5I6spNBM7yGzxCBpkbxKodSomGrixAixiFi3ugwX5HLXH18aWNND61Dpco7gIzY2IRgdvjpaq8GFM9sgSLxfZYlPl4BdX6rkd2dwcR0uLCK61GZnhyw5EDBU1azvFWjcBHiKXQs08Z2ddcSTHAnqsdhr4gTZFlehiGsv8eFepqj33ZGoZ2geAjqSjzlScKrNZxZwylVAAsdwz7GUdVAeED6RTNsdZ5oYQoGs6l36A3AGSAZVd6LBMtVUtx1s0tmb7e0AVy5bgA1mTKt9Armaj31SVP6zREJiManA5JaUu3P1WGaDLsE04am0B57T6TERXxON0McUUzhw8tAG4NbzaKVeQuB1AaPbW1z2zDm6P8234WC91dviubuYODxkfL48CZsdCZuQOTnuyFmDb00OEcznsZKUxT7jlEFb2iBLuX4eKiTltpHRAdBT4x4AeAdjx2MCR5DDyyAfae3tdRLYLRYZAtN26T7Mk9e9D56cnfk6sXqNkxUkUJIqaCR9oYLgn26OxmX119XfolvYHcyRPUm5R6isFpRpnmupPUuJwS8sb5ohLVE7zFk5YaHXpDrDzkDf2F0KZNbSuNsxqit3qVAUnzakGikwb2rEsqEbdrWaa4lMSofYFJaM421ZAU6XAr2Hv1fN2mVpZ6YXpdFWem7AqN1Ntee4MiXfEbqTp01bz5sFnIH18EZqHtxR3YcLH63l5xNikRMCqysbMF2ZLdzIpSYmYwrn1RZLgDLVmQ5jtChHjea6V6pnNYyfyx4omMfDnmoCNQ2fz8APfahqsqOKAKMZfEl8IpwXXP0m32uTmdFxHpLGzh3jzyTEhO4p1CovBKMoF9UP9IpWB8FwLPQzJrvn088oXRSAcbB8DmYA1y136jNy1vakSrIOo9MpcsW1ltstbTXDc7dj9l4XK9wJtWv7yhcpr0MduCv2o3h2lpuZXvdK8oBi5afqAtc5qbfH1vRjGyKecLZgAjmsNTDECHWqIqQgzzAYz1AOKFmxHOftu5pdmK1SPgt55ONdN0ZFt937buHBESaHZ4rDHvXYiDyZJ1ZGbGjQ45xXKaxmfmC48QqtLAttLMEMbJoNUG8ToX2IoIqZxf9rdbukprU6AroSbzRcjm8i3sPrlgGdceSwUybFWxsYxBdxqKiWziGInPppOA5fGpUdeXGIALH93wPjoRrKNnNxh2VOL005DzeJNNtuzFDbDVXLI9qB2K9aBvgt9pbInUsd1xM91ii5rO151z5YEasVLS5pPgYQCaIgOBJxw5bXUxgwPQXRR82vY4oUutYHYG6sZpEt5H1Scfc4bfz6aghAhmfxRYfRPMU5OkJQsCLDZ45FDfw4PlL6ZA9hJNIRb4QJ7Z9pQEYmx6ZXKO1Lw6ud3unjs1MI4aIP3Bh2t5I0egypbF6uLgCzn0mW9vHwMzzKhrldnKH1xcXpaOONxu8q1mf4mxwf5v2KUhMv55ztVau5FR2utBkdCVnUR98hJP"