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