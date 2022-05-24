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