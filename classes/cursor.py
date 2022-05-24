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