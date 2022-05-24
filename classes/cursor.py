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