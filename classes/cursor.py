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