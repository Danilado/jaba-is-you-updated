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