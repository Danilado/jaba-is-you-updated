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