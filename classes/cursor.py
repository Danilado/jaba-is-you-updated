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