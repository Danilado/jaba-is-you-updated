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