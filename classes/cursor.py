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