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