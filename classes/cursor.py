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