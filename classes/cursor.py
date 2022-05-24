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