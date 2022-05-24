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