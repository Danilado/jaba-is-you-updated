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