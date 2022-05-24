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