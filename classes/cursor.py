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