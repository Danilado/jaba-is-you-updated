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