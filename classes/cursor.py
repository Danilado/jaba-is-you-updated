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