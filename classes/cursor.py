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