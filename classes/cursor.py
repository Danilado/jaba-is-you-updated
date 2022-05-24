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