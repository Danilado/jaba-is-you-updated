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