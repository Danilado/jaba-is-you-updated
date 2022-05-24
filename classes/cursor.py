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