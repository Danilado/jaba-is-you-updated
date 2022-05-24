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