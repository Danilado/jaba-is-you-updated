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