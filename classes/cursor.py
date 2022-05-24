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