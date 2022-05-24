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