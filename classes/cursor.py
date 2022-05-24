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