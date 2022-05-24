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