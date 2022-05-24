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