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