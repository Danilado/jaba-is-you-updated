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