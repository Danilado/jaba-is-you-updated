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