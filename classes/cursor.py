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

"VhXwWKSkL1BpzkvIhX8262PosJviEdhx67TONkuGo2eowzuYPSnbyUnp34tb3tL1025SPS0hhSi1wyjFFBuwplmc8fF6LbJEhHwQEchpH3Rryww1azCDGbyEePpQXOYreHlTFzFnwSrolt3K5Kt40QLDFBD6SS6qnvxBCLTGbbXwEVbLJ5qjLMvU6qbHR75bTuesEWvSvb0WKESp7JrgBO8QAExSglHkcQdsHRxYXHlF0R8vF9QPIDrguAEpz9JWjPCxE1CJYcV9WLvotuDl9OXxhcXfdEe4zuvOhy9ThWkIMzO4XeFWCl0RM575NxCglbEubC9YqV5KaXdtAB3KGbEQvL8X5YbxbhHs8zAnGZybLhRvNQJKaGxfhIxVuYP0KyyWzs7KUnyPqr9XZfulbAv6qDp8AwUzlhJyMj8YRFHU8p0ZVBTxMxeAN4vJICpoVioqqhoYRnG6JsjSjln5WgSsskRLv7QVbfW1V6cHbw6Crs4GLTtLFTd2IJpJC5WF5vRZKdIrjcqrlNlYiTAiSkGh2fboHB5ouhPIqAZ2hN4mBSiZ79wnaw16aGtjYTCLVXncShq6rktGRAt71LHcsFBKFV9qF6rsngRFcS3YwaVoDIFwoDj7W9gKh1FIFreVrbS2wjcxptKQh0TFOgyV2WG4oAiwsQhZAZeoQK5k0IPJZumkluIVKsLMoDoBd3UrCJDO5L7Vh3LKC0E2sZzecYqmUgNYM1BOhevwcYHuEsSZXu1PwGsePupRUihwy8RUcrbgJJMwzaWNKAjeMIKS9TbInAi69ssK4kjD4Q1cNx2nHrByIofL4xZWDj9W2Og7JaIhwXTksF8ru5tYz6g7HeTjSgQaCD4pCAPPzxlqdl6KfuxOAc8C1navVJsz8FsyxEIeVVLQKHSV68QSrCIv6zqxxwSmMAXJWJwUsX1d45vBl6Kh8uh357Di3Gi5GBlLstBYqw4ekZWLrSacbUur4pv594Y9HR9JsXVgs9Fb0aRG3o0wY6awq8ZtGFCwRBHctLhZXKOoGDVGBNF3qabcBHg0sfDUp1IxcC3WuPTg1dLkdxA9WC2Qbh5QkjaSkli9FPnh3o9PNqJzHTv7Q0OrYStmVXYodihmT3lTAqxrROB00KNl5Pi925ZAkyx9wqP6HzeI6qsRDmmA5EYU0tPm3uKAZ1iwUixJ4L77FMjx16XJRxxDDXhaVLPjOfCA2wKlIhVoGQ8wDcgbHtam0EtxrZ4I7LL7SpBWgspjSUoTN5PeXliFg62dcTGvxdR2Q71y2hENh1xiXLtXl0cPNDUDXn9W6TeqeZCn0agrkME4MmOVsF0IESTAKh1baDXhxsEInwZLOWaDYqHvHoEazLm9i3RegPwMxkETViZFQ4sHiImBCSGLgo5c3lugZRAu5yKctGj6uQD7Pf555uzvihpSA1mC4sPnJ6QlLRGfNTqEkR4cxYNgOYU2EQgAnKLe6vbQFkgl41R8M0OaFNGkDmzyVGXTfdY"