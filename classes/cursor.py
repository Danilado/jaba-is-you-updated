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