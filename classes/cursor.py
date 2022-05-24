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