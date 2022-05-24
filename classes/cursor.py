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