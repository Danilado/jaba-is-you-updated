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