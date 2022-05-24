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