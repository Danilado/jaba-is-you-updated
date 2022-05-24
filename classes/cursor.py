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