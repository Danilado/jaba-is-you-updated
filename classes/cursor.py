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