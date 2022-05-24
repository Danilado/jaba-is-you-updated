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