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