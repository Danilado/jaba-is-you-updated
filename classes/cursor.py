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