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