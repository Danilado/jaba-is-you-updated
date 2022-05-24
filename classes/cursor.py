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