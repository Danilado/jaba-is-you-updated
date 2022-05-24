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

"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"