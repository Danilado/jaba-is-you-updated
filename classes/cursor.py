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