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