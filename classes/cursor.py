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