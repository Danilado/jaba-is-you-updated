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