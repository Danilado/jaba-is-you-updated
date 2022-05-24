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