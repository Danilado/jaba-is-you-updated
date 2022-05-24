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