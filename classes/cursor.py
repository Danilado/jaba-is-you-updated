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