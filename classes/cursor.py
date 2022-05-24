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