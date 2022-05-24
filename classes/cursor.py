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