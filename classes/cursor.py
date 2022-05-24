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