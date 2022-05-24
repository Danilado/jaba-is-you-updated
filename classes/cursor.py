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