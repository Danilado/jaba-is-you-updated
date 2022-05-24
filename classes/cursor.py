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