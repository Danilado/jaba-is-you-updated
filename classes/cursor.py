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