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