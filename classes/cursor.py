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