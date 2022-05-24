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