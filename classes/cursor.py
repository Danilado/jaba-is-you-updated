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