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