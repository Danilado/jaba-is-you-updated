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