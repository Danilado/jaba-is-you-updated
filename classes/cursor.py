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