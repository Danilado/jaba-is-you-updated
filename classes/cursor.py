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