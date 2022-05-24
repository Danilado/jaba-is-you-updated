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