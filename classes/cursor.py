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