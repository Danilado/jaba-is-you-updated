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