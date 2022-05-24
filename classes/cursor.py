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