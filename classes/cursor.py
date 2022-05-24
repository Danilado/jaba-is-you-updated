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