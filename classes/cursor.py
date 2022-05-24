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