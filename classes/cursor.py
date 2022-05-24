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