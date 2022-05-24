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