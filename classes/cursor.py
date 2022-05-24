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