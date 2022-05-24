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