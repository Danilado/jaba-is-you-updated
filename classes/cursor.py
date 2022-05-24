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