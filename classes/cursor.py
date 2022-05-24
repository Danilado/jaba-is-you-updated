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