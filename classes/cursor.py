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