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