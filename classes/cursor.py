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