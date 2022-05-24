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