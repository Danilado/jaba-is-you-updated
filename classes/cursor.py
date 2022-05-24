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