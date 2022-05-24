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