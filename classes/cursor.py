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