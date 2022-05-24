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