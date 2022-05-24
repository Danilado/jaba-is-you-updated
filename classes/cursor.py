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