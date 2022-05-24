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